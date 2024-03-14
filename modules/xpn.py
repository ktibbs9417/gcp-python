import os
from dotenv import load_dotenv
from google.cloud import (
    compute_v1
    )
from google.iam.v1 import policy_pb2
import google.auth
from google.cloud.compute_v1.types import (
    Binding,
    Policy,
    RegionSetPolicyRequest
    )


class XPN():

    def __init__(self):
        # Load the environment variables from the .env file
        load_dotenv()

        # Get the Shared VPC host project ID from the environment variable
        self.host_project_id = os.getenv('SHARED_HOST_PRJ_ID')
        self.credentials, _ = google.auth.default()
        self.service_project_id = os.getenv('GCP_PROJECT_ID')
        self.region = os.getenv('SHARED_VPC_REGION')
        self.subnet = os.getenv('SHARED_VPC_SUBNET')
        self.users = os.getenv('SHARED_VPC_USERS')
    

    def _attach_shared_vpc(self, **kwargs):
        """
        Attach a service project to a Shared VPC host project.

        Parameters:
        host_project_id (str): The ID of the Shared VPC host project.
        service_project_id (str): The ID of the service project to attach.
        """
        
        # Optionally pass the project_id that was created in another step to be used here preventing the need to fill out the .env variable
        project_id = kwargs.get('project_id', None)
        self.service_project_id = os.getenv('GCP_PROJECT_ID')
        if self.service_project_id:
            svc_prj_id = self.service_project_id
        else:
            svc_prj_id = project_id
        print(f"Attaching service project {svc_prj_id} to Shared VPC host project {self.host_project_id}")
        # Initialize the Compute Engine client
        service = compute_v1.ProjectsClient(credentials=self.credentials)

        # Construct the request to enable the Shared VPC for the service project
        request = compute_v1.EnableXpnResourceProjectRequest(
            project=self.host_project_id,
            projects_enable_xpn_resource_request_resource=compute_v1.ProjectsEnableXpnResourceRequest(
                xpn_resource=compute_v1.XpnResourceId(
                    id=svc_prj_id,
                    type_='PROJECT'  # The type can be 'PROJECT' for service projects
                )
            )
        )

        # Execute the request
        operation = service.enable_xpn_resource(request=request)

        # Wait for the operation to complete (optional)
        operation.result()

        print(f"Service project {svc_prj_id} has been attached to the Shared VPC host project {self.host_project_id}.")

    def _assign_svpc_access(self, **kwargs):
        project_id = kwargs.get('project_id', None)
        self.service_project_id = os.getenv('GCP_PROJECT_ID')
        if self.service_project_id:
            svc_prj_id = self.service_project_id
        else:
            svc_prj_id = project_id

        print(f"Assigning Shared VPC access to service project {svc_prj_id}")
        # Initialize the Compute Engine Subnetworks client
        subnet_client = compute_v1.SubnetworksClient(credentials=self.credentials)

        # Get the current IAM policy for the subnet
        policy = subnet_client.get_iam_policy(
            request={ 
            "project": self.host_project_id,
            "region": self.region,
            "resource": self.subnet,
            }
        )
                # Iterate over users to add them to the policy

        for pair in self.users.split(';'):
            principal, principal_id = pair.split(':')
            member = f"{principal}:{principal_id}"
            # Check if the binding for this role already exists
            bindings = Binding(role="roles/compute.networkUser", members=[f"{member}"])
            # Add new bindings to the policy
            policy.bindings.append(bindings)
        print(f"/compute/v1/projects/{self.host_project_id}/regions/{self.region}/subnetworks/{self.subnet}/getIamPolicy")
        print(f"Update Shared VPC Subnet policy to: {policy}")


        # Set the updated IAM policy
        response = subnet_client.set_iam_policy(
            request={
                "project": self.host_project_id,
                "region": self.region,
                "resource": self.subnet,
                "region_set_policy_request_resource": 
                    RegionSetPolicyRequest(
                        policy=Policy(
                            bindings=policy.bindings
                        )
                    )
            }
        )

        # Print the updated IAM policy for the Shared VPC Subnet
        print(f"Updated IAM policy for subnet {self.subnet} in project {svc_prj_id}:")
        print(response)