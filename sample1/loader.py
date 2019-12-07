def resource_load(*resources):
    for resource in resources:
        __import__('sample1.resource.{}'.format(resource))


def model_load(*models):
    for model in models:
        __import__('sample1.database.{}'.format(model))
