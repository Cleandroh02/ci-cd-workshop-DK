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

```
az acr webhook create --name test12345 --registry demodkagosto  --resource-group=rg_Workshop_Dataknow_Ago2023 --tags Developer="cesar higuita" --actions push --uri https://demodataknowcicdappdev.azurewebsites.net --scope "booksapi:apicicd" 
```


