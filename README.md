<div align="center">
    <h1>Marktemplate</h1>
    <p>XML -> XML preprocessor</p>
</div>

## About
Marktemplate is a preprocessor for XML, where you write XML with special `<mt-*>` tags that are processed into regular XML.

It is a very simple preprocessing library to learn and use.

## Use
### Processing a file
If you want to process a file, then you must provide a source and destination path 

```
./marktemplate.py <src> <dest>
```

### Evaluating raw text
If you want to evaluate the result of some raw marktemplate string, you can do this by providing a single argument:

```
./marktemplate.py <raw>
```

## Writing marktemplate
Marktemplate will evaluate anything in `<mt-*>` tags. Each tag does something small and specific.

### mt-attr
Attr searches for an attribute and returns a text node containing the value of that attribute. If the attribute doesn't exist, it will error out.

**USAGE:**
```xml
<mt-attr name=[attribute_name] />
```

**EXAMPLE ONE:**
```xml
<mt-attr x="value" name="x">
```

Produces:

```xml
value
```

**EXAMPLE TWO:**
```xml
<root x="y">
    <div>
        <mt-attr name="x" />
    </div>
</root>
```

Produces:

```xml
<root x="y">
    <div>
        y
    </div>
</root>
```

### mt-for

### mt-glob

### mt-include

### mt-raw-include

### mt-text-include

