from dotenv import load_dotenv
import os
import random
from google.cloud import (
    resourcemanager_v3,
    billing_v1,
    service_usage_v1,
    
    )
from google.iam.v1 import policy_pb2
from google.api_core.exceptions import GoogleAPICallError
import google.auth


class CreateProject:
    def __init__(self):
        load_dotenv()
        self.folder_id = f"folders/{os.getenv('GCP_FOLDER_ID')}"
        self.project_name = os.getenv('GCP_PROJECT_NAME')
        self.project_id = f"{self.project_name}-{random.randint(1000, 9999)}"
        self.billing_id = f"billingAccounts/{os.getenv('GCP_BILLING_ID')}"
        self.iam_principals_and_roles = os.getenv('IAM_PRINCIPALS_AND_ROLES')
        self.enable_api = os.getenv('ENABLE_API')
        self.credentials, _ = google.auth.default()
        

    def _create_project(self):
        project_client =resourcemanager_v3.ProjectsClient(credentials=self.credentials)
        try:
            prj = {
                "display_name" : self.project_name,
                "project_id" : self.project_id,
                "parent" : self.folder_id,
            }
            if self.folder_id is not None:
                prj = prj | {"parent" : self.folder_id}
            else:
                prj = prj |f"organizations/{self.folder_id}"
            
            create_project_request = resourcemanager_v3.CreateProjectRequest(
                project=prj
            )
            
            print("Creating project...")
            project_client.create_project(request=create_project_request)
            print(f"Created successfully!")
            self._set_billing_account()

        except GoogleAPICallError as e:
            print(f"Failed to create project {self.project_id}. Error: {e}")
        return self.project_id
    
    def _set_billing_account(self):
        billing_client = billing_v1.CloudBillingClient(credentials=self.credentials)
        print("Setting billing account...")
        try:
            # Construct the request to set the billing account
            request = billing_v1.UpdateProjectBillingInfoRequest(
                name=f"projects/{self.project_id}",
                project_billing_info=billing_v1.ProjectBillingInfo(billing_account_name = self.billing_id)
            )
            # Set the billing account
            billing_client.update_project_billing_info(request=request)
            print(f"Billing account set to {self.billing_id} for project {self.project_id}.")
        except GoogleAPICallError as e:
            print(f"Failed to assign billing account {self.billing_id} to project {self.project_id}. Error: {e}")
            
        
    def _enable_api(self, project_id):
        service_client = service_usage_v1.ServiceUsageClient(credentials=self.credentials)
        print("Enabling API...")
        
        # Get the list of APIs to enable from the .env file
        apis_to_enable = os.getenv('ENABLE_API').split(',')
        # Iterate over each API and enable it
        for api in apis_to_enable:
            api = api.strip()  # Remove any leading/trailing whitespace
            service_name = f"projects/{project_id}/services/{api}"

            # Construct the request to enable the service
            request = service_usage_v1.EnableServiceRequest(name=service_name)

            try:
                # Enable the service
                operation = service_client.enable_service(request=request)
                operation.result()  # Wait for the operation to complete
                print(f"Enabled API: {api} for project {project_id}")
            except GoogleAPICallError as e:
                print(f"Failed to enable API: {api} for project {project_id}. Error: {e}")

    def _assign_iam_roles(self, project_id):
        # Parse the IAM_PRINCIPALS_AND_ROLES variable
        project_client =resourcemanager_v3.ProjectsClient(credentials=self.credentials)
        bindings = []
        print("Assigning IAM roles...")
        try:
            for pair in self.iam_principals_and_roles.split(';'):
                principal, role = pair.split(',')
                member, principal_id = principal.split(':')
                role_id = role.split('/')[1]
                bindings.append(policy_pb2.Binding(role=f"roles/{role_id}", members=[f"{member}:{principal_id}"]))

            # Get the current IAM policy
            policy = project_client.get_iam_policy(request={"resource": f"projects/{project_id}"})

            # Add new bindings to the policy
            policy.bindings.extend(bindings)

            # Set the updated IAM policy
            response = project_client.set_iam_policy(
                request={
                    "resource": f"projects/{project_id}",
                    "policy": policy
                }
            )
            print("Updated IAM policy:", response)
        except GoogleAPICallError as e:
            print(f"Failed to assign IAM roles for project {project_id}. Error: {e}")
        