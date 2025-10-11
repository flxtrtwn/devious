terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.53.1"
    }
    hetznerdns = {
      source  = "timohirt/hetznerdns"
      version = "~> 2.2.0"
    }
  }

  backend "s3" {
    bucket   = "dummy"
    key      = "dummy"
    region = "nbg1"
    access_key = "dummy"
    secret_key = "dummy"
    endpoint = "https://nbg1.your-objectstorage.com"
    skip_region_validation      = true
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_requesting_account_id = true
    use_path_style = true
    skip_s3_checksum = true
  }
}

# Configure the Hetzner DNS Provider
variable "dns_token" {
  type = string
  sensitive = true
}

provider "hetznerdns" {
  apitoken = var.dns_token
}

provider "hcloud" {
  token = var.cloud_token
}

variable "cloud_token" {
  type      = string
  sensitive = true
}

variable "ssh_key_name" {
  type    = string
}

variable "domain_name" {
  type = string
}

# VM
resource "hcloud_server" "web" {
  name        = var.domain_name
  image       = "ubuntu-22.04"
  server_type = "cx22"
  location    = "nbg1"
  ssh_keys    = [var.ssh_key_name]
  user_data   = file("cloud-init.yaml")
}

#TODO: Set up DNS Zone
data "hetznerdns_zone" "zone" {
  name = ""
}

resource "hetznerdns_record" "main" {
  zone_id = data.hetznerdns_zone.zone.id
  name    = "@"
  value   = hcloud_server.web.ipv4_address
  type    = "A"
  ttl     = 3600
}

resource "hetznerdns_record" "www" {
  zone_id = data.hetznerdns_zone.zone.id
  name    = "www"substitute_pl
  value   = hcloud_server.web.ipv4_address
  type    = "A"
  ttl     = 3600
}

# Output for Ansible
output "ansible_inventory" {
  value = {
    all = {
      hosts = {
        web = {
          ansible_host = hcloud_server.web.ipv4_address
          ansible_user = "deploy"
          ansible_ssh_private_key_file = "~/.ssh/id_rsa"
        }
      }
    }
  }
}
