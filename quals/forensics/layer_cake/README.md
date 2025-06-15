# Layer Cake

## Challenge (100 points, 373 solves)

> Layer cake is so good. I have an mp3 file all about layer cake. Maybe you can find the flag there?
>
> Author: lyrisng

## Summary

An mp3 file is given, but is it actually an mp3 file?

## Analysis

```bash
$ file "dist/layer cake.mp3"
dist/layer cake.mp3: Zip archive data, made by v2.0 UNIX, extract using at least v2.0, last modified Fri Mar 30 19:37:05 2018, method=store
```

## Approach

Unzip the file to see its contents.

```bash
$ unzip "dist/layer cake.mp3"
Archive:  dist/layer cake.mp3
file #1:  bad zipfile offset (local header sig):  0
   creating: /Users/ncduy/Git/greyctf25-writeup/quals/forensics/Layer Cake/layers/docProps
  inflating: layers/docProps/app.xml  
  inflating: layers/docProps/core.xml  
   creating: /Users/ncduy/Git/greyctf25-writeup/quals/forensics/Layer Cake/layers/word
  inflating: layers/word/document.xml  
  inflating: layers/word/fontTable.xml  
  inflating: layers/word/settings.xml  
  inflating: layers/word/styles.xml  
   creating: /Users/ncduy/Git/greyctf25-writeup/quals/forensics/Layer Cake/layers/word/theme
  inflating: layers/word/theme/theme1.xml  
  inflating: layers/word/webSettings.xml  
   creating: /Users/ncduy/Git/greyctf25-writeup/quals/forensics/Layer Cake/layers/word/_rels
  inflating: layers/word/_rels/document.xml.rels  
  inflating: layers/[Content_Types].xml  
   creating: /Users/ncduy/Git/greyctf25-writeup/quals/forensics/Layer Cake/layers/_rels
  inflating: layers/_rels/.rels   
```

Use `grep` to search for the flag in the unzipped files.

```bash
$ grep -ro 'grey{[^}]*}' layers/
layers/word/styles.xml:grey{s0_f3w_lay3r5_w00p5}
```

## Flag

`grey{s0_f3w_lay3r5_w00p5}`
