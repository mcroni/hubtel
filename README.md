A Python interface for the Hubtel Payment API.
Contributed by Kojo Mcroni




### Receive MOMO
```
import Hubtel
p = Hubtel("username","password","merchant")
request = p.receive("kojo mcroni","027180861x","kojo_mcroni@xxx.com","tigo-gh",5,"http://xxxx.com/callback","for lola rae",fees=True,cl_reg)
  
print(request)

```
