```bash
kubectl apply -f chatbot-deployment.yaml
kubectl apply -f sentiment-analysis-api-deployment.yaml
kubectl apply -f chatbot-service.yaml
kubectl apply -f sentiment-analysis-api-service.yaml
kubectl apply -f chatbot-hpa.yaml
kubectl apply -f sentiment-analysis-api-hpa.yaml

```