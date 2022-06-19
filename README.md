# Spotifiuby back\_queue\_metrics

[![codecov](https://codecov.io/gh/TallerII-Grupo11/back_queue_metrics/branch/main/graph/badge.svg?token=5CIK0SM2UN)](https://codecov.io/gh/TallerII-Grupo11/back_queue_metrics)
[![Linters](https://github.com/TallerII-Grupo11/back_queue_metrics/actions/workflows/linter.yaml/badge.svg)](https://github.com/TallerII-Grupo11/back_queue_metrics/actions/workflows/linter.yaml)
[![Tests](https://github.com/TallerII-Grupo11/back_queue_metrics/actions/workflows/test.yaml/badge.svg)](https://github.com/TallerII-Grupo11/back_queue_metrics/actions/workflows/test.yaml)
[![Deploy](https://github.com/TallerII-Grupo11/back_queue_metrics/actions/workflows/deploy.yaml/badge.svg)](https://github.com/TallerII-Grupo11/back_queue_metrics/actions/workflows/deploy.yaml)


### Docker

Run app commands local
```
docker build -t back-queue-metric .
docker run -p 5000:5000 --env-file .env back-queue-metric
```

### Manual Deploy to Heroku

[Heroku]()

```
heroku config:set port=5000
heroku config:set title="Back Queue Metric"

heroku container:push web -a spotifiuby-queue-metric
heroku container:release web -a spotifiuby-queue-metric

```

### Test

Run tests using [pytest](https://docs.pytest.org/en/6.2.x/)

``` bash
pytest tests/
```
