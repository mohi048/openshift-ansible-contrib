OpenShift on OpenStack
======================

Requirements
------------

* Ansible 2.2
  - we depend on the `os_stack` module introduced in 2.2
  - http://docs.ansible.com/ansible/os_stack_module.html
* Shade >= 1.8.0
  - a Python library to talk to the OpenStack APIs
  - the `os_stack` module depends on it

LBaaS v2
--------

http://docs.openstack.org/newton/networking-guide/config-lbaas.html

