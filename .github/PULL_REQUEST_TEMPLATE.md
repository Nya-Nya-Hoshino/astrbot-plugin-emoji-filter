## Description

<!-- Briefly describe your changes -->

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Performance improvement
- [ ] Documentation update

## Testing

<!-- How did you verify your changes? -->

`
[emoji_filter] Plugin loaded. enabled=true
[emoji_filter] on_decorating_result triggered (priority=100)
[emoji_filter] Emoji stripped: ...
`

## Checklist

- [ ] _EMOJI_PATTERN still covers all Unicode emoji blocks
- [ ] Priority remains > 0 to run before downstream plugins
- [ ] python -c "import ast; ast.parse(open('main.py').read())" passes