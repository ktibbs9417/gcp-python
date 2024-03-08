import os
from dotenv import load_dotenv
from google.cloud import compute_v1


class XPN:

    def attach_shared_vpc(host_project_id, service_project_id):
        """
        Attach a service project to a Shared VPC host project.

        Parameters:
        host_project_id (str): The ID of the Shared VPC host project.
        service_project_id (str): The ID of the service project to attach.
        """
        # Initialize the Compute Engine client
        service = compute_v1.ProjectsClient()

        # Construct the request to enable the Shared VPC for the service project
        request = compute_v1.EnableXpnResourceProjectRequest(
            project=host_project_id,
            projects_enable_xpn_resource_request_resource=compute_v1.ProjectsEnableXpnResourceRequest(
                xpn_resource=compute_v1.XpnResourceId(
                    id=service_project_id,
                    type_='PROJECT'  # The type can be 'PROJECT' for service projects
                )
            )
        )

        # Execute the request
        operation = service.enable_xpn_resource(request=request)

        # Wait for the operation to complete (optional)
        operation.result()

        print(f"Service project {service_project_id} has been attached to the Shared VPC host project {host_project_id}.")
