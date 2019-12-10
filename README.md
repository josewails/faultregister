### Azure create resource group

Create a resource group which is the container where all our resources will live

    `az group create --name faultRegister --location "West Europe"`

Result:

```json

{
  "id": "/subscriptions/35b5f50c-e7b6-41d7-a893-2f9ad478e0c1/resourceGroups/faultRegister",
  "location": "westeurope",
  "managedBy": null,
  "name": "faultRegister",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null,
  "type": null
}
```

Create mysql Server

`az mysql server create --resource-group faultRegister --name fault-register --location "West Europe" --admin-user marcin --admin-password zarathustra-2901  --sku-name B_Gen5_1`

Result: 

```json
{
  "administratorLogin": "marcin",
  "earliestRestoreDate": "2019-06-15T13:53:16.913000+00:00",
  "fullyQualifiedDomainName": "fault-rregister.mysql.database.azure.com",
  "id": "/subscriptions/35b5f50c-e7b6-41d7-a893-2f9ad478e0c1/resourceGroups/faultRegister/providers/Microsoft.DBforMySQL/servers/fault-rregister",
  "location": "westeurope",
  "masterServerId": "",
  "name": "fault-register",
  "replicaCapacity": 5,
  "replicationRole": "None",
  "resourceGroup": "faultRegister",
  "sku": {
    "capacity": 1,
    "family": "Gen5",
    "name": "B_Gen5_1",
    "size": null,
    "tier": "Basic"
  },
  "sslEnforcement": "Enabled",
  "storageProfile": {
    "backupRetentionDays": 7,
    "geoRedundantBackup": "Disabled",
    "storageAutoGrow": "Disabled",
    "storageMb": 5120
  },
  "tags": null,
  "type": "Microsoft.DBforMySQL/servers",
  "userVisibleState": "Ready",
  "version": "5.7"
}
```

Configure firewall settings

`az mysql server firewall-rule create --name allAzureIPs --server fault-register --resource-group faultRegister --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0`

Result: 

```json
{
  "endIpAddress": "0.0.0.0",
  "id": "/subscriptions/35b5f50c-e7b6-41d7-a893-2f9ad478e0c1/resourceGroups/faultRegister/providers/Microsoft.DBforMySQL/servers/fault-register/firewallRules/allAzureIPs",
  "name": "allAzureIPs",
  "resourceGroup": "faultRegister",
  "startIpAddress": "0.0.0.0",
  "type": "Microsoft.DBforMySQL/servers/firewallRules"
}
```

Create a firewall to allow access for my IP

`az mysql server firewall-rule create --name allowLocalClient --server fault-register --resource-group faultRegister --start-ip-address 193.140.239.55 --end-ip-address 193.140.239.55`

Result: 

```json
{
  "endIpAddress": "193.140.239.55",
  "id": "/subscriptions/35b5f50c-e7b6-41d7-a893-2f9ad478e0c1/resourceGroups/faultRegister/providers/Microsoft.DBforMySQL/servers/fault-register/firewallRules/allowLocalClient",
  "name": "allowLocalClient",
  "resourceGroup": "faultRegister",
  "startIpAddress": "193.140.239.55",
  "type": "Microsoft.DBforMySQL/servers/firewallRules"
}
```

Create a plan.

`az appservice plan create --name faultRegisterPlan --resource-group faultRegister --sku B1 --is-linux`

Result: 


```json
{
  "freeOfferExpirationTime": "2019-07-15T14:39:34.263333",
  "geoRegion": "West Europe",
  "hostingEnvironmentProfile": null,
  "hyperV": false,
  "id": "/subscriptions/35b5f50c-e7b6-41d7-a893-2f9ad478e0c1/resourceGroups/faultRegister/providers/Microsoft.Web/serverfarms/faultRegisterPlan",
  "isSpot": false,
  "isXenon": false,
  "kind": "linux",
  "location": "West Europe",
  "maximumElasticWorkerCount": 1,
  "maximumNumberOfWorkers": 3,
  "name": "faultRegisterPlan",
  "numberOfSites": 0,
  "perSiteScaling": false,
  "provisioningState": "Succeeded",
  "reserved": true,
  "resourceGroup": "faultRegister",
  "sku": {
    "capabilities": null,
    "capacity": 1,
    "family": "B",
    "locations": null,
    "name": "B1",
    "size": "B1",
    "skuCapacity": null,
    "tier": "Basic"
  },
  "spotExpirationTime": null,
  "status": "Ready",
  "subscription": "35b5f50c-e7b6-41d7-a893-2f9ad478e0c1",
  "tags": null,
  "targetWorkerCount": 0,
  "targetWorkerSizeId": 0,
  "type": "Microsoft.Web/serverfarms",
  "workerTierName": null
}
```

Create a deployment user. 

`az webapp deployment user set --user-name marcin-deploy --password zarathustra-2901`

Result: 

```json
{
  "id": null,
  "kind": null,
  "name": "web",
  "publishingPassword": null,
  "publishingPasswordHash": null,
  "publishingPasswordHashSalt": null,
  "publishingUserName": "marcin-deploy",
  "scmUri": null,
  "type": "Microsoft.Web/publishingUsers/web"
}
```

Create a webapp

`az webapp create --resource-group faultRegister --plan faultRegisterPlan --name faultregister --runtime "PYTHON|3.7" --deployment-local-git`

Result: 

```json

{
  "availabilityState": "Normal",
  "clientAffinityEnabled": true,
  "clientCertEnabled": false,
  "clientCertExclusionPaths": null,
  "cloningInfo": null,
  "containerSize": 0,
  "dailyMemoryTimeQuota": 0,
  "defaultHostName": "faultregister.azurewebsites.net",
  "deploymentLocalGitUrl": "https://marcin-deploy@faultregister.scm.azurewebsites.net/faultregister.git",
  "enabled": true,
  "enabledHostNames": [
    "faultregister.azurewebsites.net",
    "faultregister.scm.azurewebsites.net"
  ],
  "ftpPublishingUrl": "ftp://waws-prod-am2-085.ftp.azurewebsites.windows.net/site/wwwroot",
  "geoDistributions": null,
  "hostNameSslStates": [
    {
      "hostType": "Standard",
      "ipBasedSslResult": null,
      "ipBasedSslState": "NotConfigured",
      "name": "faultregister.azurewebsites.net",
      "sslState": "Disabled",
      "thumbprint": null,
      "toUpdate": null,
      "toUpdateIpBasedSsl": null,
      "virtualIp": null
    },
    {
      "hostType": "Repository",
      "ipBasedSslResult": null,
      "ipBasedSslState": "NotConfigured",
      "name": "faultregister.scm.azurewebsites.net",
      "sslState": "Disabled",
      "thumbprint": null,
      "toUpdate": null,
      "toUpdateIpBasedSsl": null,
      "virtualIp": null
    }
  ],
  "hostNames": [
    "faultregister.azurewebsites.net"
  ],
  "hostNamesDisabled": false,
  "hostingEnvironmentProfile": null,
  "httpsOnly": false,
  "hyperV": false,
  "id": "/subscriptions/35b5f50c-e7b6-41d7-a893-2f9ad478e0c1/resourceGroups/faultRegister/providers/Microsoft.Web/sites/faultregister",
  "identity": null,
  "inProgressOperationId": null,
  "isDefaultContainer": null,
  "isXenon": false,
  "kind": "app,linux",
  "lastModifiedTimeUtc": "2019-06-15T14:45:35.780000",
  "location": "West Europe",
  "maxNumberOfWorkers": null,
  "name": "faultregister",
  "outboundIpAddresses": "13.81.108.99,52.232.76.83,52.166.73.203,52.233.173.39,52.233.159.48",
  "possibleOutboundIpAddresses": "13.81.108.99,52.232.76.83,52.166.73.203,52.233.173.39,52.233.159.48,51.144.4.170,51.144.79.142",
  "redundancyMode": "None",
  "repositorySiteName": "faultregister",
  "reserved": true,
  "resourceGroup": "faultRegister",
  "scmSiteAlsoStopped": false,
  "serverFarmId": "/subscriptions/35b5f50c-e7b6-41d7-a893-2f9ad478e0c1/resourceGroups/faultRegister/providers/Microsoft.Web/serverfarms/faultRegisterPlan",
  "siteConfig": null,
  "slotSwapStatus": null,
  "state": "Running",
  "suspendedTill": null,
  "tags": null,
  "targetSwapSlot": null,
  "trafficManagerHostNames": null,
  "type": "Microsoft.Web/sites",
  "usageState": "Normal"
}
```

Set environment variables


`az webapp config appsettings set --name faultregister --resource-group faultRegister --settings DBHOST="fault-register.mysql.database.azure.com" DBUSER="marcin@fault-register" DBPASS="zarathustra-2901" DBNAME="fault_register"`

Result: 

```json
[
  {
    "name": "DBHOST",
    "slotSetting": false,
    "value": "fault-register.mysql.database.azure.com"
  },
  {
    "name": "DBUSER",
    "slotSetting": false,
    "value": "marcin@fault-register"
  },
  {
    "name": "DBPASS",
    "slotSetting": false,
    "value": "zarathustra-2901"
  },
  {
    "name": "DBNAME",
    "slotSetting": false,
    "value": "fault_register"
  }
]
```