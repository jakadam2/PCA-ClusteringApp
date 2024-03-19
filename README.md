# API documentation


```js
// DTOs
variable = {
    "id":int,
    "name":string,
    "typeId":int[0|1],
    "values":[double]
    }

dataset = {
    "datasetname":string,
    "variables":[variable],
    "normalizationMethodId":int
    }

dataType = {
    "id":int[0|1],  // numerical or categorical
    "name":string
    }

normalizationMethod = {
    "id":int,
    "name":string,
    "typeId":int[0|1]
    }

clusteringAlgorithm = {
    "id":int,
    "name":string
    }

clusteringDescription = {
    "graph":image,
    "description":string
    }
```



## /file

### POST
send .csv dataset to server

### GET
download exported .csv dataset


## /dataset?valuesQuantity=n

### GET
return overview of analyzed dataset: `data` with only n values for each variable

### PUT
update dataset overview



## /components/graph
returns graph



## /normalizationMethods

### GET
return list of available normalization methods: `[normalizationMethods]`



## /dataTypes

### GET
return list of available dataTypes: `[dataType]`



## /clustering/

### POST
upload list of chosen variables ids along with chosen clustering method id

## GET
return image with string describing it


## /clustering/methods

### GET
return list of cluesting methods