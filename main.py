from modules.create_project import CreateProject
    

project_id = CreateProject()._create_project()
CreateProject()._enable_api(project_id)
CreateProject()._assign_iam_roles(project_id)