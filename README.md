# ci-cd-workshop-DK


## The Wrokflow

```
mkdir -p .github/workflows
```

## Secrets Container Registry

```
az acr update -n demodkagosto --admin-enabled true
```
```
az acr credential show -n demodkagosto
```