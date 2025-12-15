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
./marktemplate.py <src> -o <dest>
```

### Evaluating raw text
If you want to evaluate the result of some raw marktemplate string, you can do this by providing no arguments and using `stdin`:

```
echo "<root />" | ./marktemplate.py
```

## Writing marktemplate
Marktemplate will evaluate anything in `<mt-*>` tags. Each tag does something small and specific.

### mt-attr
Attr searches for an attribute and returns a text node containing the value of that attribute. If the attribute doesn't exist, it will error out.

**USAGE:**
```xml
<mt-attr name=[attribute_name] />
```

**EXAMPLE ONE: Fetching the value of x**
```xml
<mt-attr x="value" name="x">
```

Produces:

```xml
value
```

**EXAMPLE TWO: Fetching the value of x from muliple nested blocks away**
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
For runs a for loop - copying the inner children of the for block each time, while also setting an attribute to the current iteration number.

**EXAMPLE ONE: Running a basic for loop**
```xml
<root>
    <mt-for start="0" stop="10">
        <mt-attr name="i" />
    </mt-for>
</root>
```

Produces:

```xml
<root>
    0
    1
    2   
    3
    4
    5
    6
    7
    8
    9
</root>
```
**EXAMPLE TWO: Specifying the step count**

**EXAMPLE THREE: Specifying the variable count**

### mt-glob
Glob searches for all files/directories that match a glob syntax

**EXAMPLE**

```xml
<root>
    <mt-glob src="*.txt">
        <file> <mt-attr name="src" /> </file>
    </mt-glob>
</root>
```

Produces:

```xml
<root>
    <file>file1.txt</file>
    <file>file2.txt</file>
    <file>file3.txt</file>
    ...
</root>
```


### mt-include
Include parses a file as xml, then processes it as mt - inserting the result into the DOM.

**EXAMPLE**

Lets say we have a file called `sub.xml`:
```xml
<div x="5">
    <mt-attr name="x"/>
    <h1>Hello!</h1>
</div>
```

Then: 

```xml
<root>
    <mt-include src="./sub.xml" />
</root>
```

Produces:

```xml
<root>
    <div x="5">
        5
        <h1>Hello!</h1>
    </div>
</root>
```

### mt-raw-include
Raw include parses a file as xml, and inserts it into the DOM.

**EXAMPLE**

Lets say we have a file called `sub.xml`:
```xml
<div x="5">
    <mt-attr name="x"/>
    <h1>Hello!</h1>
</div>
```

Then: 

```xml
<root>
    <mt-include src="./sub.xml" />
</root>
```

Produces:

```xml
<root>
    #text "<div x="5">\n\t\t5\n\t\t<h1>Hello!</h1>\n\t</div>"
</root>
```

### mt-text-include
Include reads a file and includes it as a text node in the DOM tree. This means it won't be evaluated.

**EXAMPLE**

Lets say we have a file called `sub.xml`:
```xml
<div x="5">
    <mt-attr name="x"/>
    <h1>Hello!</h1>
</div>
```

Then: 

```xml
<root>
    <mt-include src="./sub.xml" />
</root>
```

Produces:

```xml
<root>
    #text "<div x="5">\n\t\t<mt-attr name="x"/>\n\t\t<h1>Hello!</h1>\n\t</div>"
</root>
```
