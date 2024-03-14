
<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">Project Creation</h3>

  <p align="center">
    This script will assist with the creation of a GCP Project. Please review all steps that are taken to ensure that when the script is executed you are aware of all actions that will be taken place.
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li>
      <a href="#prerequisites">Prerequisites</a>
      <ul>
        <li><a href="#iam-roles">IAM Roles</a></li>
        <li><a href="#cloud-sdk-installation">Cloud SDK Installation</a></li>
        <li><a href="#virtualenv-installation">Virtualenv Installation</a></li>
        <li><a href="#populate-the-env-file">Populate the ENV file</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
  </ol>
</details>



<!-- Getting Started -->
## Getting Started


There are a few steps that need to be taken to ensure that you have the appropriate permissions, configurations, and libraries prior to executing the script.

Requirements:

1. [Download, Install, and Sign into CloudSDK](https://cloud.google.com/sdk/docs/install)

2. [Create a virtualenv using pip](https://virtualenv.pypa.io/en/latest/)
  
   * virtualenv is a tool to create isolated Python environments. Be sure to use Python 3.11 
   
3. Install python dependencies
4. Verify code and execute
5. Have the permissions to create projects within GCP


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Prerequisites


This is an example of how to sign into Cloud SDK and create a virtualenv.

### IAM Roles
Project Creator role is required at the Org or Folder level.
The Billing User role is required on the billing account itself.
```sh
roles/resourcemanager.projectCreator
roles/billing.user
```
#### Using Shared VPC
If you are needing to create a project that needs to have access to a Shared VPC, the account running this script will need to have the following IAM Role [here](https://console.cloud.google.com/networking/xpn/details)

```sh
roles/compute.xpnAdmin
```

### Required APIs
APIs must be enabled on the project you are using to authenticate to when executing this script.
```sh
cloudbilling.googleapis.com
```

### Cloud SDK Installation

1. Download one of the following:
   * [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

2. Initialize gcloud
  
   _it is recommended that you already have a project created within GCP which you use to test and use as a playground since this will help with authentication if you are running this script locally_
   ```sh
   gcloud init
   ```
3. Create local authentication credentials for your Google Account
   ```sh
   gcloud auth application-default login
   ```
   _A login screen is displayed. After you log in, your credentials are stored in the local credential file used by ADC. For more information about working with ADC in a local environment, see [Local development environment](https://cloud.google.com/iam/docs/authentication#:~:text=local%20environment%2C%20see-,Local%20development%20environment,-.)._

### Virtualenv Installation
#### Mac/Linux

```
pip3 install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install google-api-python-client
```

#### Windows

```
pip install virtualenv
virtualenv <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install google-api-python-client
```

### Populate the ENV file
Within the working directory there is a `.env` which contains the following that need to be filled out prior to execution.
```sh
# Specify if you are creating a new project or not
CREATE_PROJECT=True
# Attach project to shared VPC
SHARED_VPC_ACCESS=True
# GCP Folder ID
GCP_FOLDER_ID=<folder-id>
# GCP Project Name not unique
GCP_PROJECT_NAME=<project-name>
# GCP Project ID please leave blank if you do not have this yet! Used if you are not creating a new project
GCP_PROJECT_ID=<project-id>
# GCP Billing ID
GCP_BILLING_ID=<billing-id>
# List of Principals e.g. "user:user@examples.com,roles/storage.admin;group:group@examples.com,roles/viewer"
IAM_PRINCIPALS_AND_ROLES="user:user@example.com,roles/editor;serviceAccount:svc@example.com,roles/appengine.appAdmin;group:group@example.com,roles/viewer"
# List of APIs to enable e.g. "compute.googleapis.com,run.googleapis.com"
ENABLE_API="compute.googleapis.com,run.googleapis.com"
# List of users to be able to access the Shared VPC e.g. "user:user@examples.com,roles/storage.admin;group:group@examples.com,roles/viewer"
SHARED_VPC_USERS="user:user@example.com,roles/editor;serviceAccount:svc@example.com,roles/appengine.appAdmin;group:group@example.com,roles/viewer"
# The Region of the Shared VPC Subnet
SHARED_VPC_REGION=us-west2
# The Subnet of the Shared VPC
SHARED_VPC_SUBNET=us-west-la-dev

```

### Intall Dependencies
```sh
pip install -r requirements.txt
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

After all the Prerequities have been completed, execute the script:
```sh
python3 create_project.py
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

For now the script will be passed around but it is highly recommended to place it within its own repository.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT 
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-->

<!-- ACKNOWLEDGMENTS 
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->