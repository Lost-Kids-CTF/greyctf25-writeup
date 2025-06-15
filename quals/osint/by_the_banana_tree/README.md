# By The Banana Tree

## Challenge (100 points, 169 solves)

> I saw a church in the distance while travelling. Can you tell me where it is?
>
> The flag consists of latitude and longitude coordinates of the location where the photo was taken, rounded to three decimal places, and the name of the church in the distance in lowercase (according to google maps, omitting any potential spaces, punctuation and diacritics).
>
> Regarding flag format, consider this example for Notre Dame de Paris: grey{N48-853_E2-349_notredamecathedralofparis}
>
> Author: k-hian

## Summary

Find the source of this image.

![By The Banana Tree](dist/bythebananatree.png)

## Analysis

Google Image Reverse Search is not enough here. Need to do some manual analysis of the image.

## Approach

Look at the landmark sign to find the street name in Vietnam. There are two streets: QL.32 and DT.317. Use Google Maps to look for all churches around 12km away from the intersection of these two streets. After that, just try to do manual image matching with the satellite view of the area.

## Flag

`grey{N21-153_E105-274_nhathothanhlam}`
