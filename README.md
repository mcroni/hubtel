This is an Unofficial Python interface for the Hubtel Payment API.
Contributed by Kojo Mcroni


### Installation
To install simple type ```pip install hubtel```


#### Receive MOMO

[You can find exclusive documentation on Hubtel's website,, here ](https://developers.hubtel.com/documentations/merchant-account-api#receive-money)
```
import Hubtel
p = Hubtel("username","password","merchant")
request = p.receive("kojo mcroni","027180861x","kojo_mcroni@xxx.com","tigo-gh",5,"http://xxxx.com/callback","for lola rae",fees=True,cl_reg)
  
print(request)

```






