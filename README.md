# ACR_Token_POC
POC documentation and notes for the use of Azure Container Registry with scoped registry access tokens.  
The goal is to create an implementation which supports the creation of tokens scoped to individual repositories via REST API, pending their inclusion in our SDKs.

Tokens should be provided to customers / users to download specific images from the registry, to deploy in their own environments, without being bound to a deployment in Azure.

Examples are given in Python to quickly show the formatting of the API requests, as REST client was quick to create.

During the POC we shall explore using other languages and frameworks as needed.

## Documentation

You can find the Rest API spec and example requests to create and manage tokens on a repo here:
**NOTE**: The properties field is important in the top level, and contains the request parameters.

[azure-rest-api-specs/ScopeMapCreate.json](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/containerregistry/resource-manager/Microsoft.ContainerRegistry/preview/2021-08-01-preview/examples/ScopeMapCreate.json)  
[azure-rest-api-specs/TokenCreate.json](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/containerregistry/resource-manager/Microsoft.ContainerRegistry/preview/2021-08-01-preview/examples/TokenCreate.json)

### Figuring things out:

#### Portal:

To view the scopemap/token json , you can try exporting templates from azure portal.
Navigate to the registry resource, under automation, click on Export template, from the exported template you will find the json representation of scopemap and tokens from your registry.

#### CLI:

You will also be able to view the cli request payload with the cli -debug command.  
Sample command:  
```az acr token create --name tokenName -r registryName  --scope-map _repositories_pull --debug```

Az Cli impelementation for reference: 
https://github.com/Azure/azure-cli/blob/dev/src/azure-cli/azure/cli/command_modules/acr/token.py

#### REST:

See token operations available in the API via

https://docs.microsoft.com/en-us/rest/api/containerregistry/operations/list

i.e. using PostMan:  
```GET https://management.azure.com/providers/Microsoft.ContainerRegistry/operations?api-version=2019-05-01```


## Using the sample code

In the sample, we have created an app registration in the Azure portal, in our AAD tenant, and are using this to create and modify tokens.

For this to work, the app was given rights to the Azure Container Registry to perform these operations.

You can install the required python modules using :

```pip install -r ./requirements.txt```

Sample API calls can be found under ```./src/ACR_Rest_Client.py```

The current Python module for ACR is available here, but at the time of the POC and writing, did not contain the necessary classes and functions for managing Token access.

https://docs.microsoft.com/en-us/python/api/overview/azure/containerregistry-readme?view=azure-python-preview

