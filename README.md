"# chatRasa" 
"# chatRasa" 

-pour entrainer le modele

-pour lancer l'api rasa
rasa run -m models --enable-api --cors "*" --debug


-pour actier les acrions et permettre une recherche intelligente 

rasa run actions --debug


curl -X POST http://localhost:11434/api/generate -d '{"model":"mistral","prompt":"À qui est destinée la plateforme E-Carrière ?"}'



 
