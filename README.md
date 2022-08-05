# api

[![Build](https://github.com/ionite34/api/actions/workflows/build.yml/badge.svg)](https://github.com/ionite34/api/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/ionite34/api/branch/main/graph/badge.svg?token=er4KGsaRMZ)](https://codecov.io/gh/ionite34/api)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ionite34/api/main.svg)](https://results.pre-commit.ci/latest/github/ionite34/api/main)

![Deployed][deployed_badge]

[![License][fossa_small]][fossa_small_ref]
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

## A collection of experimental endpoints and utilities
```python
api.ionite.io
```

### Full Documentation at [api.ionite.io/docs](https://api.ionite.io/docs)

## Rickroll detection
> Powered by [rolldet][rolldet_gh]

### `rolldet/{url}`

- Returns json data for detecting whether URLs resolve to rick-rolls

```http request
GET https://api.ionite.io/rolldet/www.youtube.com/watch?v=VZrDxD0Za9I

{"url":"https://www.youtube.com/watch?v=VZrDxD0Za9I","redirectUrl":null,"isRoll":true,"error":null,"song":"Never Gonna Give You Up (7\" Mix)","artist":"Rick Astley"}
```



## License
The code in this project is released under the [MIT License](LICENSE).

[![FOSSA Status](https://app.fossa.com/api/projects/custom%2B31224%2Fgithub.com%2Fionite34%2Fapi.svg?type=large)](https://app.fossa.com/projects/custom%2B31224%2Fgithub.com%2Fionite34%2Fapi?ref=badge_large)

[rolldet_gh]: https://github.com/ionite34/rolldet
[deployed_badge]: https://img.shields.io/github/v/release/ionite34/api?label=Deployed&logo=googlecloud&logoColor=lightblue&sort=semver
[fossa_small]: https://app.fossa.com/api/projects/custom%2B31224%2Fgithub.com%2Fionite34%2Fapi.svg?type=small
[fossa_small_ref]: https://app.fossa.com/projects/custom%2B31224%2Fgithub.com%2Fionite34%2Fapi?ref=badge_small
