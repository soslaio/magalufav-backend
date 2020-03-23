sudo docker-compose -f stack.yml up -d --build
echo "Aguardando inicialização dos containers..."
sleep 15
echo "Executando scripts de migração..."
sudo docker exec -it magalu-api sh -c "python manage.py migrate"
sudo docker exec -it magalu-api sh -c "echo \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@magazineluiza.com.br', 'admin_pass')\" | python manage.py shell"
echo "Tudo pronto!"