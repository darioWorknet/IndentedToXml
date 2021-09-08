# Indented text to xml

This project prettends to create a tool whose input is an indented text .txt and whose output is the conversion to XML format. All this having into account that labels can store variables and values.

An example of input/output could be the following:

input:
```txt
a
    b variable=var1
        b1 variable=var2 Some text
        b2
```

output:
```xml
<a>
    <b variable=var1>
        <b1 variable=var2> Some text </b1>
        <b2> --- </b2>
    </b>
</a>
```
