# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

    # Copy the SSH key to the VM(s):
    config.vm.provision "shell" do |s|
      ssh_pub_key = File.readlines("#{Dir.home}/.ssh/id_rsa.pub").first.strip
      s.inline = <<-SHELL
        echo #{ssh_pub_key} >> /home/vagrant/.ssh/authorized_keys
        mkdir -p /root/.ssh/
        echo #{ssh_pub_key} >> /root/.ssh/authorized_keys
      SHELL
    end

    config.vm.define "hub", autostart: false do |hub|
        hub.vm.box = "ubuntu/focal64"
        hub.vm.hostname = "hub"
        hub.vm.network "private_network", ip: "192.168.56.2"
        hub.ssh.insert_key = true
        hub.vm.provider "virtualbox" do |v|
            v.memory = 2048
            v.cpus = 4
        end
    end
end
