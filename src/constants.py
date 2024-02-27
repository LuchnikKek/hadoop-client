BASE_URI = 'http://{host}:{port}/webhdfs/v1'  # noqa

# Endpoints
LS_URI = BASE_URI + '/{path}?op=LISTSTATUS'
MKDIR_URI = BASE_URI + '/{path}?op=MKDIRS&permission={permission}&user.name={owner}'
