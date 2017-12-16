bootstrap:
	ansible-playbook -u root -i inventories/hosts.ini playbooks/bootstrap.yml

setup-master:
	ansible-playbook -u root -i inventories/hosts.ini playbooks/master.yml

setup-frontend:
	ansible-playbook -u root -i inventories/hosts.ini playbooks/frontend.yml

deploy:
	ansible-playbook -u root -i inventories/hosts.ini playbooks/deploy.yml

rollback:
	ansible-playbook -u root -i inventories/hosts.ini playbooks/rollback.yml
