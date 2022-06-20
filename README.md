# back_queue_metrics

## UP

```
docker-compose -f docker-compose.yml up --build
```

## DOWN

```
docker-compose -f docker-compose.yml down
```

## Heroku

```
heroku config:set port=5000
heroku config:set title="Back Queue Metric"
heroku config:set broker="redis://redis:6379"

heroku container:push web -a spotifiuby-queue-metric
heroku container:release web -a spotifiuby-queue-metric
```