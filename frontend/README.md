this is frontends folders.
Frontend is written in TypeScript and uses Vite as build system utility.

# building static files

```shell
npm install && npm run build
```

The command above will install dependencies and run the build process. Bundle
files would be automatically installed to the `backend/src/static` directory. 

# manually running as server
This provides ability to support `HMR` - `Hot module reload`. It means that 
backend gets the latest frontend source files, as soon as they were modified, 
and automatically refreshes the page. Working both in standalone and 
containerized modes.

Steps below are required if you want to run frontend as standalone.

1.  install the dependencies and run frontend's server:
    ```shell
    npm install && npm run build
    ```

2.  after that backend must be runned with `FRONTEND_HMR` equal to the true 
    value (either 'true' or '1').
    ```shell
    python manage.py runserver
    ```