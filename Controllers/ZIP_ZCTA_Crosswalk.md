#ZIP_ZCTA_Crosswalk

-	Uses the zip_zcta_crosswalk service.

-	Defines only one route:
```python
@ROUTE.route('/api/v1/zip-zcta-crosswalk', methods=["POST"])
```

-	In this context crosswalk does not mean zebra crossing but rather a mapping between two related data standards or systems.

-	If a ZIP code is provided, it is being converted into a ZCTA code; The contrary is valid too – if a ZCTA code is present it will be mapped into a ZIP code.

-	If the conversion fails a relevant error response is returned – bad input!
