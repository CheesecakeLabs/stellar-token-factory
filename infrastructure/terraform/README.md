# Infra

This repository contains the [Terraform](https://terraform.io) definition to create the
infrastructure in the cloud.

The environments are separated by [Terraform workspace](https://www.terraform.io/docs/state/workspaces.html).

### Requirements

- [Terraform 0.15.4](https://releases.hashicorp.com/terraform/0.15.4/terraform_0.15.4_darwin_amd64.zip)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [AWS Access Keys](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys "AWS Access Keys")

## Getting Started

### AWS Profile

To run the infrastructure with Terraform, it is essential to have a credential with sufficient rights to create the resources in the Cloud's provider. In this case, we need to have an user with an [access key and secret key from AWS generated](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys "access key and secret key from AWS generated").

If you have this programmatic credentials, you can configure them in your machine through AWS CLI using your terminal. Replace **{project_name}** with the project name:
`aws configure --profile {project_name}`

After you type this command, it will ask the "AWS Access Key ID", "AWS Secret Access Key" and "Default region name". Answer according to the project specifications.

### Terraform Backend

Terraform has a feature called [State](https://www.terraform.io/language/state "State"), that basically persists the state of resources managed by Terraform. The State can be stored in a [Backend](https://www.terraform.io/language/settings/backends "Backend"), in this project we are using S3 and DynamoDB. 

- To create it, follow the step-by-step bellow:
  - `cd setup`
  - `terraform init`
  - `terraform apply` - Confirm with a "yes"

If you have created the project with Cookiecutter and have filled the variables correctly, S3 bucket and DynamoDB should be created with the variables informed. The outputs for the `terraform apply` should be:
```shell
bucket = <stellar-tf>-terraform-state
dynamodb_table = <stellar-tf>-terraform-locks
```

This two resources are fundamental to store the Terraform State, so it is important to determine if they are successfully created and if the outputs values corresponds to the params "bucket" and "dynamodb_table" from the main.tf present in the root directory of this project (`./main.tf`). The values should be the same, so Terraform State can be saved correctly.

### Key pair generation

To access EC2 instances in AWS it is necessary to have a key pair generated, in the next steps we are going to create one for the project:

- Type the command below in your terminal. Replace **{project-env}** for Project Name and environment: 
`$ ssh-keygen -N "" -m PEM -f ~/.ssh/{project-env}`
- Get the public key value to use in the next step. Replace **{project-env}** for Project and environment:
	 ```
	$ ssh-keygen -y -f ~/.ssh/{project-env}
	ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC5u................
	 ```

**ATTENTION!** It is very important to save the public and private key files in the **Password Management tool** (today, Keeper Security), in the folder associated with the project.

**Key pair generation example:**
```shell
$ ssh-keygen -N "" -m PEM -f ~/.ssh/project_test
$ ls -la ~/.ssh/project_test*
-rw-------  1 alanmonteiro  staff  2459 Jan 24 13:46 /Users/alanmonteiro/.ssh/project_test
-rw-r--r--  1 alanmonteiro  staff   576 Jan 24 13:46 /Users/alanmonteiro/.ssh/project_test.pub
```
In this example, "**/Users/alanmonteiro/.ssh/project_test**" is the private key and "**/Users/alanmonteiro/.ssh/project_test.pub**" is the public key.

### Setting up Terraform

Now that you have the [Profile](#aws-profile "Profile"), [Backend](#terraform-backend "Backend") and [Key Pair](#key-pair-generation "Key Pair") you can setup Terraform to create the infrastructure:
- Navigate to the root directory of this project
- Initialize terraform in your local machine: `terraform init`
- Select the workspace using `terraform workspace select {env}`. **Remember**, the workspace is equivalent to the environment (dev, lab, staging, production), so replace **{env}** with the name of the environment that will be deployed
  - To list the existing workspaces use `terraform workspace list`
  - You can create new workspaces with `terraform workspace new`
- "**[Tfvars](https://www.terraform.io/language/values/variables#variable-definitions-tfvars-files "Tfvars")**" are special files to set a lot of variables in a Project. Create a `./{env}.tfvars` file (**{env} **must be replaced with the environment name, you are going to have a tfvars file for each environment that you will create) and populate it with input variables present on `./variables.tf`. One of the variables is a "public_key", fill this variable with the public key result of the "[Key pair generation](#key-pair-generation "Key pair generation")" step (ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC5u.........).


### Creating the infrastucture

Now that you have Terraform configured, you can start deploying the infrastructure:
- The first resource that you need to create is the SSL Certificate to use in Load Balancer. This resource requires a DNS validation, so you need to create the resource and access the AWS Console to get the DNS records to add them to your DNS provider.
	- Verify what will be changed. Replace **{tfvars-file}** with the tfvars filename created: `terraform plan --target="module.acm" -var-file={tfvars-file}`
	- If everything is ok, run `terraform apply --target="module.acm" -var-file={tfvars-file}`

After the command conclusion, access [AWS console](https://console.aws.amazon.com/ "AWS console"), go to "AWS Certificate Manager" and check the certificate created. The status should be "Pending". Get the informations about the certificate [to validate through DNS](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html "to validate through DNS").

After the DNS validation, the status must change to "Issued". You can continue the Infrastructure deployment:
- To verify what will be changed, run `terraform plan -var-file={tfvars-file}`
- If everything is ok, run `terraform apply -var-file={tfvars-file}` and confirm.
- The update takes some time... So, go drink a coffee ☕️.
- To get the outputs (deploy keys, container repos and DNS, use `terraform output`)

### Variables

There are some features that could be enabled/disabled through variables:
|  Variable | Description  | Type  | Default  |
| ------------ | ------------ | ------------ | ------------ |
| postgres_config.enable  | Create Postgres database for App  | bool  | false  |
| services_config.#service_name#.features.http  | Enable Load Balancer for the Service  | bool  | -  |
| services_config.#service_name#.features.force_https_redirect  | Create a HTTPS redirection in the Load Balancer for the Service  | bool  | -  |
| services_config.#service_name#.features.service_discovery  | Create Service Discovery for the service  | bool  | -  |
| kong_config.enabled  | Create Kong API Gateway Infrastructure  | bool  | false |
| bastion_config.enabled  | Create Bastion Host Infrastructure  | bool  | true |

### Security Groups
<table>
<thead>
  <tr>
    <th>Security Group</th>
    <th>Description</th>
    <th>Rule</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>module.security.public_security_group_id</td>
    <td>For external Access in Load Balancer</td>
    <td>Ingress: Source: 0.0.0.0/0 -&gt; Ports: 80/443<br><br>Egress: Destination: 0.0.0.0/0 -&gt; Ports: ALL</td>
  </tr>
  <tr>
    <td>module.security.private_security_group_id</td>
    <td>If var.bastion_config.enabled is true and var.bastion_config.security_group.private is true, allow Bastion Security Group access.<br><br>If var.kong_config.enabled is true, allow Kong Security Group access, else allow Public Security Group access.</td>
    <td>Bastion: Ingress: Source: Bastion Security Group -&gt; Ports: ALL<br><br>Kong enabled: Ingress: Source: Kong Security Group -&gt; Ports: All <br> <br>Kong disabled: Ingress: Source: Public Security Group -&gt; Ports: All <br><br>Egress: Destination: 0.0.0.0/0 -&gt; Ports: ALL</td>
  </tr>
  <tr>
    <td>module.security.database_security_group_id</td>
    <td>Allow Private Security Group access.<br><br>If var.bastion_config.enabled is true and var.bastion_config.security_group.database is true, allow Bastion Security Group access.</td>
    <td>Private: Ingress: Source: Private Security Group -&gt; Ports: ALL<br><br>Bastion: Ingress: Source: Bastion Security Group -&gt; Ports: ALL<br><br>Egress: Destination: 0.0.0.0/0 -&gt; Ports: ALL</td>
  </tr>
  <tr>
    <td>module.security.kong_private_security_group_id</td>
    <td>If var.kong_config.enabled is true, enable access to Public Security Group, Bastion Security Group and the self group</td>
    <td>Bastion: Ingress: Source: Bastion Security Group -&gt; Ports: 1337/8000-8001<br><br>Public: Ingress: Source: Public Security Group -&gt; Ports: 8000<br><br>Self: Ingress: Source: Kong Private Security Group -&gt; Ports: 8001<br><br>Egress: Destination: 0.0.0.0/0 -&gt; Ports: ALL</td>
  </tr>
  <tr>
    <td>module.security.kong_database_security_group_id</td>
    <td>If var.kong_config.enabled is true, enable access to Kong Private Security Group</td>
    <td>Private: Ingress: Source: Kong Private Security Group -&gt; Ports: 5432<br><br>Egress: Destination: 0.0.0.0/0 -&gt; Ports: ALL</td>
  </tr>
  <tr>
    <td>module.security.bastion_public_security_group_id</td>
    <td>If var.bastion_config.enabled is true, allow var.bastion_config.allowed_cidr access.</td>
    <td>Bastion: Ingress: Source: var.bastion_config.allowed_cidr -&gt; Ports: 22<br><br>Egress: Destination: 0.0.0.0/0 -&gt; Ports: ALL</td>
  </tr>
  <tr>
    <td>module.security.frontend_public_security_group_id</td>
    <td>If var.kong_config.enabled is true and there are some services that need to use Load Balancer (Example: a Frontend service that is not going stay behind Kong. var.service_config.features.http is true), enable access to Public Security Group</td>
    <td>Public: Ingress: Source: Public Security Group -&gt; Ports: var.service_config.container_port<br><br>Egress: Destination: 0.0.0.0/0 -&gt; Ports: ALL</td>
  </tr>
</tbody>
</table>

### Suggested architectures

#### Networking, databases, services and Kong API Gateway
![Alt text](docs/HA-with-Kong.jpeg?raw=true 'with-kong')

#### Networking, databases and services
![Alt text](docs/HA.jpeg?raw=true 'without-kong')

### More info

This setup creates an ECS cluster, S3 bucket, Bastion Host, Kong API Gateway, RDS database (besides all the underlying structure needed to run it: load balancer, roles, networks, security
groups, etc.).

To create new services on the cluster, check `main.tf` and follow the
same steps used to create the `backend_service` and `frontend_service`.
