from modules.create_project import CreateProject
from modules.xpn import XPN
import os
from dotenv import load_dotenv


class ProjectManager():
    def __init__(self):
        print("Starting Project Manager")
        load_dotenv()
        self.create_project = os.getenv("CREATE_PROJECT")
        print(f"Using the following environment variables:")
        print(f"CREATE_PROJECT: {self.create_project}")
        self.shared_vpc_access = os.getenv("SHARED_VPC_ACCESS")
        print(f"SHARED_VPC_ACCESS: {self.shared_vpc_access}")

    def main(self):

        # Create a new project and assign it to a Shared VPC
        if self.create_project == "True" and self.shared_vpc_access == "True":
            print("Creating project and attaching to a Shared VPC Host")
            project_id = CreateProject()._create_project()
            CreateProject()._enable_api(project_id)
            CreateProject()._assign_iam_roles(project_id)
            XPN()._attach_shared_vpc(project_id=project_id)
            XPN()._assign_svpc_access(project_id=project_id)

        # You want to create a new project and not assign a Shared VPC
        elif self.create_project == "True" and self.shared_vpc_access == "False":
            project_id = CreateProject()._create_project()
            CreateProject()._enable_api(project_id)
            CreateProject()._assign_iam_roles(project_id)

        # There is an existing project and you just want to enable APIs and assign IAM Roles and assign to a Shared VPC
        elif self.create_project == "False" and self.shared_vpc_access == "True":
            if os.getenv('GCP_PROJECT_ID') is not None:
                CreateProject()._enable_api(os.getenv('GCP_PROJECT_ID'))
                CreateProject()._assign_iam_roles(os.getenv('GCP_PROJECT_ID'))
                XPN()._attach_shared_vpc(project_id = os.getenv('GCP_PROJECT_ID'))
                XPN()._assign_svpc_access(project_id = os.getenv('GCP_PROJECT_ID'))
            else:
                print("Please update the GCP_PROJECT_ID within the .env file to contain the unique Project ID, no the Project Name")  
                print("More information about the unique Project ID can be found here: https://cloud.google.com/resource-manager/docs/creating-managing-projects#before_you_begin")          
        
        # Assign APIs and IAM Roles to an existing GCP Project
        elif self.create_project == "False" and self.shared_vpc_access == "False":
            print("Enabling APIs and assigning IAM Roles")
            if os.getenv('GCP_PROJECT_ID') is not None:
                CreateProject()._enable_api(os.getenv('GCP_PROJECT_ID'))
                CreateProject()._assign_iam_roles(os.getenv('GCP_PROJECT_ID'))
            else:
                print("Please update the GCP_PROJECT_ID within the .env file to contain the unique Project ID, no the Project Name")  
                print("More information about the unique Project ID can be found here: https://cloud.google.com/resource-manager/docs/creating-managing-projects#before_you_begin")

if __name__ == "__main__":
    ProjectManager().main()

