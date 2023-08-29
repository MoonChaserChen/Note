# Sublime插件
## Pretty Json
https://packagecontrol.io/packages/Pretty%20JSON
### 缩进风格
#### Allman indentation style
`bracket_newline = true`
```
while (x == y)
{
    something();
    something_else();
}
```
#### 1TBS (OTBS)
`bracket_newline = false`
```
void check_negative(x) {
    if (x < 0) {
        puts("Negative");
    } else {
        nonnegative(x);
    }
}
```