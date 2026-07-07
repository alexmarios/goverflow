### Configure Build with Options

Source: https://www.postgresql.org/docs/current/install-meson.html

Examples of setting the installation prefix, build type, and SSL support during setup.

```shell
# configure with a different installation prefix
meson setup build --prefix=/home/user/pg-install

# configure to generate a debug build
meson setup build --buildtype=debug

# configure to build with OpenSSL support
meson setup build -Dssl=openssl


```

--------------------------------

### PostgreSQL Installation: Short Version

Source: https://www.postgresql.org/docs/current/install-make.html

This snippet provides a quick, step-by-step guide for building and installing PostgreSQL from source. It covers configuration, compilation, installation, and initial database setup.

```shell
./configure
make
su
make install
adduser postgres
mkdir -p /usr/local/pgsql/data
chown postgres /usr/local/pgsql/data
su - postgres
/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
/usr/local/pgsql/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
/usr/local/pgsql/bin/createdb test
/usr/local/pgsql/bin/psql test
```

--------------------------------

### Quick Start Installation with Meson

Source: https://www.postgresql.org/docs/current/install-meson.html

A complete sequence of commands to configure, build, install, and initialize a PostgreSQL instance.

```shell
meson setup build --prefix=/usr/local/pgsql
cd build
ninja
su
ninja install
adduser postgres
mkdir -p /usr/local/pgsql/data
chown postgres /usr/local/pgsql/data
su - postgres
/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
/usr/local/pgsql/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
/usr/local/pgsql/bin/createdb test
/usr/local/pgsql/bin/psql test


```

--------------------------------

### Complete crosstab Example with Data Setup

Source: https://www.postgresql.org/docs/current/tablefunc.html

A full example demonstrating table creation, data insertion, and a crosstab query to pivot specific attributes into columns, including the expected output.

```SQL
CREATE TABLE ct(id SERIAL, rowid TEXT, attribute TEXT, value TEXT);
INSERT INTO ct(rowid, attribute, value) VALUES('test1','att1','val1');
INSERT INTO ct(rowid, attribute, value) VALUES('test1','att2','val2');
INSERT INTO ct(rowid, attribute, value) VALUES('test1','att3','val3');
INSERT INTO ct(rowid, attribute, value) VALUES('test1','att4','val4');
INSERT INTO ct(rowid, attribute, value) VALUES('test2','att1','val5');
INSERT INTO ct(rowid, attribute, value) VALUES('test2','att2','val6');
INSERT INTO ct(rowid, attribute, value) VALUES('test2','att3','val7');
INSERT INTO ct(rowid, attribute, value) VALUES('test2','att4','val8');

SELECT *
FROM crosstab(
  'select rowid, attribute, value
   from ct
   where attribute = ''att2'' or attribute = ''att3''
   order by 1,2')
AS ct(row_name text, category_1 text, category_2 text, category_3 text);

 row_name | category_1 | category_2 | category_3
----------+------------+------------+------------
 test1    | val2       | val3       |
 test2    | val6       | val7       |
(2 rows)
```

--------------------------------

### BEGIN simple transaction example

Source: https://www.postgresql.org/docs/current/sql-begin.htm

Basic example of starting a transaction block. All subsequent statements execute within this transaction until COMMIT or ROLLBACK is issued.

```sql
BEGIN;
```

--------------------------------

### C Example: libpq Binary I/O and Parameter Handling (testlibpq3.c)

Source: https://www.postgresql.org/docs/current/libpq-example.html

This snippet provides helper functions for a libpq example program (testlibpq3.c) that demonstrates out-of-line parameters and binary I/O. It includes setup comments for a test1 table and a function show_binary_results to process binary-formatted query results.

```C
/*
 * src/test/examples/testlibpq3.c
 *
 *
 * testlibpq3.c
 *      Test out-of-line parameters and binary I/O.
 *
 * Before running this, populate a database with the following commands
 * (provided in src/test/examples/testlibpq3.sql):
 *
 * CREATE SCHEMA testlibpq3;
 * SET search_path = testlibpq3;
 * SET standard_conforming_strings = ON;
 * CREATE TABLE test1 (i int4, t text, b bytea);
 * INSERT INTO test1 values (1, 'joe''s place', '\000\001\002\003\004');
 * INSERT INTO test1 values (2, 'ho there', '\004\003\002\001\000');
 *
 * The expected output is:
 *
 * tuple 0: got
 *  i = (4 bytes) 1
 *  t = (11 bytes) 'joe's place'
 *  b = (5 bytes) \000\001\002\003\004
 *
 * tuple 0: got
 *  i = (4 bytes) 2
 *  t = (8 bytes) 'ho there'
 *  b = (5 bytes) \004\003\002\001\000
 */

#ifdef WIN32
#include <windows.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/types.h>
#include "libpq-fe.h"

/* for ntohl/htonl */
#include <netinet/in.h>
#include <arpa/inet.h>


static void
exit_nicely(PGconn *conn)
{
    PQfinish(conn);
    exit(1);
}

/*
 * This function prints a query result that is a binary-format fetch from
 * a table defined as in the comment above.  We split it out because the
 * main() function uses it twice.
 */
static void
show_binary_results(PGresult *res)
{
    int         i,
                j;
    int         i_fnum,
                t_fnum,
                b_fnum;

    /* Use PQfnumber to avoid assumptions about field order in result */
    i_fnum = PQfnumber(res, "i");
    t_fnum = PQfnumber(res, "t");
    b_fnum = PQfnumber(res, "b");

    for (i = 0; i < PQntuples(res); i++)
    {
        char       *iptr;
        char       *tptr;
        char       *bptr;
        int         blen;
        int         ival;

        /* Get the field values (we ignore possibility they are null!) */
        iptr = PQgetvalue(res, i, i_fnum);
        tptr = PQgetvalue(res, i, t_fnum);
        bptr = PQgetvalue(res, i, b_fnum);

        /*
         * The binary representation of INT4 is in network byte order, which
         * we'd better coerce to the local byte order.
         */
        ival = ntohl(*((uint32_t *) iptr));

        /*
         * The binary representation of TEXT is, well, text, and since libpq
         * was nice enough to append a zero byte to it, it'll work just fine
         * as a C string.
         *
```

--------------------------------

### dblink_fetch Usage Example with Sequential Fetches

Source: https://www.postgresql.org/docs/current/contrib-dblink-fetch.html

Complete example showing connection setup, cursor opening, and multiple sequential fetch operations. Demonstrates how the cursor position advances with each fetch and returns fewer rows when approaching the end.

```sql
SELECT dblink_connect('dbname=postgres options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_open('foo', 'select proname, prosrc from pg_proc where proname like ''bytea%''');
 dblink_open
-------------
 OK
(1 row)

SELECT * FROM dblink_fetch('foo', 5) AS (funcname name, source text);
 funcname |  source
----------+----------
 byteacat | byteacat
 byteacmp | byteacmp
 byteaeq  | byteaeq
 byteage  | byteage
 byteagt  | byteagt
(5 rows)

SELECT * FROM dblink_fetch('foo', 5) AS (funcname name, source text);
 funcname  |  source
-----------+-----------
 byteain   | byteain
 byteale   | byteale
 bytealike | bytealike
 bytealt   | bytealt
 byteane   | byteane
(5 rows)

SELECT * FROM dblink_fetch('foo', 5) AS (funcname name, source text);
  funcname  |   source
------------+------------
 byteanlike | byteanlike
 byteaout   | byteaout
(2 rows)

SELECT * FROM dblink_fetch('foo', 5) AS (funcname name, source text);
 funcname | source
----------+--------
(0 rows)
```

--------------------------------

### GET DESCRIPTOR - Complete Usage Example

Source: https://www.postgresql.org/docs/current/ecpg-sql-get-descriptor.html

Full procedural example demonstrating GET DESCRIPTOR usage including descriptor allocation, cursor declaration, data fetching, and information retrieval for a SELECT query.

```APIDOC
## GET DESCRIPTOR - Complete Example

### Description
Complete example demonstrating the full workflow of executing a SELECT query, allocating a descriptor, fetching results, and retrieving descriptor information.

### Workflow
1. Declare host variables for descriptor data
2. Connect to database
3. Allocate a descriptor area
4. Declare and open a cursor for SELECT query
5. Fetch results into the descriptor
6. Retrieve descriptor header information (COUNT)
7. Retrieve column-specific information (RETURNED_OCTET_LENGTH, DATA)
8. Close cursor and deallocate descriptor

### Code Example
```c
int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    int  d_count;
    char d_data[1024];
    int  d_returned_octet_length;
EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO testdb AS con1 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL ALLOCATE DESCRIPTOR d;

    /* Declare, open a cursor, and assign a descriptor to the cursor  */
    EXEC SQL DECLARE cur CURSOR FOR SELECT current_database();
    EXEC SQL OPEN cur;
    EXEC SQL FETCH NEXT FROM cur INTO SQL DESCRIPTOR d;

    /* Get a number of total columns */
    EXEC SQL GET DESCRIPTOR d :d_count = COUNT;
    printf("d_count                 = %d\n", d_count);

    /* Get length of a returned column */
    EXEC SQL GET DESCRIPTOR d VALUE 1 :d_returned_octet_length = RETURNED_OCTET_LENGTH;
    printf("d_returned_octet_length = %d\n", d_returned_octet_length);

    /* Fetch the returned column as a string */
    EXEC SQL GET DESCRIPTOR d VALUE 1 :d_data = DATA;
    printf("d_data                  = %s\n", d_data);

    /* Closing */
    EXEC SQL CLOSE cur;
    EXEC SQL COMMIT;

    EXEC SQL DEALLOCATE DESCRIPTOR d;
    EXEC SQL DISCONNECT ALL;

    return 0;
}
```

### Output Example
```
d_count                 = 1
d_returned_octet_length = 6
d_data                  = testdb
```
```

--------------------------------

### PostgreSQL libpq connection and parameterized query with binary data

Source: https://www.postgresql.org/docs/current/libpq-example.html

Complete C program demonstrating libpq connection setup, error handling, secure search path configuration, and two parameterized query examples: text parameters with binary results, and binary parameters with binary results. Requires libpq development libraries and proper connection parameters.

```C
int
main(int argc, char **argv)
{
    const char *conninfo;
    PGconn     *conn;
    PGresult   *res;
    const char *paramValues[1];
    int         paramLengths[1];
    int         paramFormats[1];
    uint32_t    binaryIntVal;

    /*
     * If the user supplies a parameter on the command line, use it as the
     * conninfo string; otherwise default to setting dbname=postgres and using
     * environment variables or defaults for all other connection parameters.
     */
    if (argc > 1)
        conninfo = argv[1];
    else
        conninfo = "dbname = postgres";

    /* Make a connection to the database */
    conn = PQconnectdb(conninfo);

    /* Check to see that the backend connection was successfully made */
    if (PQstatus(conn) != CONNECTION_OK)
    {
        fprintf(stderr, "%s", PQerrorMessage(conn));
        exit_nicely(conn);
    }

    /* Set always-secure search path, so malicious users can't take control. */
    res = PQexec(conn, "SET search_path = testlibpq3");
    if (PQresultStatus(res) != PGRES_COMMAND_OK)
    {
        fprintf(stderr, "SET failed: %s", PQerrorMessage(conn));
        PQclear(res);
        exit_nicely(conn);
    }
    PQclear(res);

    /*
     * The point of this program is to illustrate use of PQexecParams() with
     * out-of-line parameters, as well as binary transmission of data.
     *
     * This first example transmits the parameters as text, but receives the
     * results in binary format.  By using out-of-line parameters we can avoid
     * a lot of tedious mucking about with quoting and escaping, even though
     * the data is text.  Notice how we don't have to do anything special with
     * the quote mark in the parameter value.
     */

    /* Here is our out-of-line parameter value */
    paramValues[0] = "joe's place";

    res = PQexecParams(conn,
                       "SELECT * FROM test1 WHERE t = $1",
                       1,       /* one param */
                       NULL,    /* let the backend deduce param type */
                       paramValues,
                       NULL,    /* don't need param lengths since text */
                       NULL,    /* default to all text params */
                       1);      /* ask for binary results */

    if (PQresultStatus(res) != PGRES_TUPLES_OK)
    {
        fprintf(stderr, "SELECT failed: %s", PQerrorMessage(conn));
        PQclear(res);
        exit_nicely(conn);
    }

    show_binary_results(res);

    PQclear(res);

    /*
     * In this second example we transmit an integer parameter in binary form,
     * and again retrieve the results in binary form.
     *
     * Although we tell PQexecParams we are letting the backend deduce
     * parameter type, we really force the decision by casting the parameter
     * symbol in the query text.  This is a good safety measure when sending
     * binary parameters.
     */

    /* Convert integer value "2" to network byte order */
    binaryIntVal = htonl((uint32_t) 2);

    /* Set up parameter arrays for PQexecParams */
    paramValues[0] = (char *) &binaryIntVal;
    paramLengths[0] = sizeof(binaryIntVal);
    paramFormats[0] = 1;        /* binary */

    res = PQexecParams(conn,
                       "SELECT * FROM test1 WHERE i = $1::int4",
                       1,       /* one param */
                       NULL,    /* let the backend deduce param type */
                       paramValues,
                       paramLengths,
                       paramFormats,
                       1);      /* ask for binary results */

    if (PQresultStatus(res) != PGRES_TUPLES_OK)
    {
        fprintf(stderr, "SELECT failed: %s", PQerrorMessage(conn));
        PQclear(res);
        exit_nicely(conn);
    }

    show_binary_results(res);

    PQclear(res);

    /* close the connection to the database and cleanup */
    PQfinish(conn);

    return 0;
}
```

--------------------------------

### Setup Type and Language for Transform Example

Source: https://www.postgresql.org/docs/current/sql-createtransform.html

Before creating a transform, the target data type (e.g., hstore) and the procedural language (e.g., plpython3u) must be defined or enabled in the database.

```sql
CREATE TYPE hstore ...;

CREATE EXTENSION plpython3u;
```

--------------------------------

### Install PostgreSQL documentation with make install-docs

Source: https://www.postgresql.org/docs/current/install-make.html

Installs HTML and man page documentation for PostgreSQL.

```bash
make install-docs
```

--------------------------------

### Start PostgreSQL Tutorial with psql

Source: https://www.postgresql.org/docs/current/tutorial-sql-intro.html

Start the psql client in single-step mode for the 'mydb' database and load the basic SQL commands from 'basics.sql'.

```bash
$ **psql -s mydb**

...

mydb=> **\i basics.sql**
```

--------------------------------

### CREATE TRANSFORM - Example with hstore and plpython3u

Source: https://www.postgresql.org/docs/current/sql-createtransform.html

Practical example demonstrating how to create a transform for the hstore data type with the plpython3u procedural language. Shows the complete workflow including type creation, language setup, function definitions, and transform creation.

```APIDOC
## CREATE TRANSFORM - hstore Example

### Description
Complete example of creating a transform for the `hstore` type and `plpython3u` language, including setup of the type, language, conversion functions, and the transform itself.

### Step 1: Create the Type and Language
```sql
CREATE TYPE hstore ...;

CREATE EXTENSION plpython3u;
```

### Step 2: Create the Conversion Functions
```sql
CREATE FUNCTION hstore_to_plpython(val internal) RETURNS internal
LANGUAGE C STRICT IMMUTABLE
AS ...;

CREATE FUNCTION plpython_to_hstore(val internal) RETURNS hstore
LANGUAGE C STRICT IMMUTABLE
AS ...;
```

### Step 3: Create the Transform
```sql
CREATE TRANSFORM FOR hstore LANGUAGE plpython3u (
    FROM SQL WITH FUNCTION hstore_to_plpython(internal),
    TO SQL WITH FUNCTION plpython_to_hstore(internal)
);
```

### Notes
- In practice, these commands would be wrapped up in an extension
- The `contrib` section contains extensions that provide transforms, which can serve as real-world examples
```

--------------------------------

### VACUUM Examples

Source: https://www.postgresql.org/docs/current/sql-vacuum.htm

Practical examples demonstrating how to use the VACUUM command with various options for table maintenance and optimization.

```APIDOC
## VACUUM Examples

### Example 1: Clean and Analyze Single Table
Clean a single table `onek`, analyze it for the optimizer, and print a detailed vacuum activity report:

```sql
VACUUM (VERBOSE, ANALYZE) onek;
```

### Legacy Syntax (PostgreSQL 9.0 and earlier)
The following syntax was used before PostgreSQL version 9.0 and is still supported:

```sql
VACUUM [ FULL ] [ FREEZE ] [ VERBOSE ] [ ANALYZE ] [ table_and_columns [, ...] ]
```

**Note:** In this legacy syntax, options must be specified in exactly the order shown.
```

--------------------------------

### Start cygserver on Cygwin

Source: https://www.postgresql.org/docs/current/installation-platform-notes.html

Start this program to provide shared memory support. It must be running whenever you start the PostgreSQL server or initialize a database cluster.

```shell
/usr/sbin/cygserver &
```

--------------------------------

### CONNECT Command Examples with Various Parameters

Source: https://www.postgresql.org/docs/current/ecpg-sql-connect.html

Provides multiple examples of the `CONNECT` command, showcasing different ways to specify connection targets, names, and user credentials, including direct values and host variables.

```sql
EXEC SQL CONNECT TO "connectdb" AS main;
EXEC SQL CONNECT TO "connectdb" AS second;
EXEC SQL CONNECT TO "unix:postgresql://200.46.204.71/connectdb" AS main USER connectuser;
EXEC SQL CONNECT TO "unix:postgresql://localhost/connectdb" AS main USER connectuser;
EXEC SQL CONNECT TO 'connectdb' AS main;
EXEC SQL CONNECT TO 'unix:postgresql://localhost/connectdb' AS main USER :user;
EXEC SQL CONNECT TO :db AS :id;
EXEC SQL CONNECT TO :db USER connectuser USING :pw;
EXEC SQL CONNECT TO @localhost AS main USER connectdb;
EXEC SQL CONNECT TO REGRESSDB1 as main;
EXEC SQL CONNECT TO AS main USER connectdb;
EXEC SQL CONNECT TO connectdb AS :id;
EXEC SQL CONNECT TO connectdb AS main USER connectuser/connectdb;
EXEC SQL CONNECT TO connectdb AS main;
EXEC SQL CONNECT TO connectdb@localhost AS main;
EXEC SQL CONNECT TO tcp:postgresql://localhost/ USER connectdb;
EXEC SQL CONNECT TO tcp:postgresql://localhost/connectdb USER connectuser IDENTIFIED BY connectpw;
EXEC SQL CONNECT TO tcp:postgresql://localhost:20/connectdb USER connectuser IDENTIFIED BY connectpw;
EXEC SQL CONNECT TO unix:postgresql://localhost/ AS main USER connectdb;
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb AS main USER connectuser;
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb USER connectuser IDENTIFIED BY "connectpw";
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb USER connectuser USING "connectpw";
EXEC SQL CONNECT TO unix:postgresql://localhost/connectdb?connect_timeout=14 USER connectuser;
```

--------------------------------

### Install tsm_system_time extension

Source: https://www.postgresql.org/docs/current/tsm-system-time.html

Required setup to enable the SYSTEM_TIME sampling method in the current database.

```sql
CREATE EXTENSION tsm_system_time;

```

--------------------------------

### Use a custom postgresql.conf for temporary installations

Source: https://www.postgresql.org/docs/current/regress-run.html

Supply a pre-written configuration file to a temporary installation using the --temp-config flag.

```shell
echo 'log_checkpoints = on' > test_postgresql.conf
echo 'work_mem = 50MB' >> test_postgresql.conf
make check EXTRA_REGRESS_OPTS="--temp-config=test_postgresql.conf"

```

--------------------------------

### Install PostgreSQL world build with make install-world

Source: https://www.postgresql.org/docs/current/install-make.html

Installs PostgreSQL and documentation when the world target was built previously.

```bash
make install-world
```

--------------------------------

### Install PostgreSQL world build without documentation with make install-world-bin

Source: https://www.postgresql.org/docs/current/install-make.html

Installs PostgreSQL binaries only when the world target was built without documentation.

```bash
make install-world-bin
```

--------------------------------

### Install PostgreSQL with make install

Source: https://www.postgresql.org/docs/current/install-make.html

Standard installation command that installs PostgreSQL files into directories specified during configuration. Typically requires root permissions.

```bash
make install
```

--------------------------------

### Install PostgreSQL with ninja

Source: https://www.postgresql.org/docs/current/install-meson.html

Run the basic installation command after building PostgreSQL. Requires appropriate write permissions to the target directories, which may require root access.

```bash
ninja install
```

--------------------------------

### Install PostgreSQL client-only components

Source: https://www.postgresql.org/docs/current/install-make.html

Installs only client applications, interface libraries, and documentation. Use when server installation is not needed.

```bash
make -C src/bin install
make -C src/include install
make -C src/interfaces install
make -C doc install
```

--------------------------------

### Start new PostgreSQL database server

Source: https://www.postgresql.org/docs/current/upgrading.html

Start the newly initialized PostgreSQL server. Ensure you are logged in as the special database user.

```bash
/usr/local/pgsql/bin/postgres -D /usr/local/pgsql/data
```

--------------------------------

### Start PostgreSQL Server with pg_ctl

Source: https://www.postgresql.org/docs/current/app-pg-ctl.html

Basic command to start the PostgreSQL server and wait until it accepts connections. Use this for standard server startup.

```bash
$ pg_ctl start
```

--------------------------------

### Example PL/pgSQL Trigger Function and Table Setup

Source: https://www.postgresql.org/docs/current/plpgsql-trigger.html

Demonstrates creating a table and a trigger function for data validation and auditing. Trigger functions must be declared with no arguments and return the 'trigger' type.

```sql
CREATE TABLE emp (
    empname           text,
    salary            integer,
    last_date         timestamp,
    last_user         text
);

CREATE FUNCTION emp_stamp() RETURNS trigger AS $emp_stamp$
    BEGIN
        -- Check that empname and salary are given
        IF NEW.empname IS NULL THEN
            RAISE EXCEPTION 'empname cannot be null';
        END IF;
```

--------------------------------

### Configure PostgreSQL autostart on OpenBSD

Source: https://www.postgresql.org/docs/current/server-start.html

Add this block to /etc/rc.local to verify binary existence and start the server during the boot sequence.

```shell
if [ -x /usr/local/pgsql/bin/pg_ctl -a -x /usr/local/pgsql/bin/postgres ]; then
    su -l postgres -c '/usr/local/pgsql/bin/pg_ctl start -s -l /var/postgresql/log -D /usr/local/pgsql/data'
    echo -n ' postgresql'
fi

```

--------------------------------

### Build and Install sepgsql Regression Test Policy (Shell)

Source: https://www.postgresql.org/docs/current/sepgsql.html

These commands build the `sepgsql-regtest` policy package from its source and then install it using `semodule`. The `semodule -l` command verifies successful installation.

```shell
$ cd .../contrib/sepgsql
$ make -f /usr/share/selinux/devel/Makefile
$ sudo semodule -u sepgsql-regtest.pp
$ sudo semodule -l | grep sepgsql
sepgsql-regtest 1.07
```

--------------------------------

### Install Documentation Tools on FreeBSD using pkg

Source: https://www.postgresql.org/docs/current/docguide-toolsets.html

This command installs the required DocBook XML, XSL, libxslt, and FOP packages on FreeBSD systems.

```bash
pkg install docbook-xml docbook-xsl libxslt fop
```

--------------------------------

### Build and Install All PostgreSQL Contrib Modules

Source: https://www.postgresql.org/docs/current/contrib.html

Run these commands in the `contrib` directory of a configured source tree to build and install all optional components.

```bash
**make**
**make install**
```

--------------------------------

### CREATE EXTENSION Command Synopsis

Source: https://www.postgresql.org/docs/current/sql-createextension.html

This is the general syntax for the `CREATE EXTENSION` command, showing all available parameters for installing an extension.

```sql
CREATE EXTENSION [ IF NOT EXISTS ] _extension_name_
    [ WITH ] [ SCHEMA _schema_name_ ]
             [ VERSION _version_ ]
             [ CASCADE ]
```

--------------------------------

### Run PostgreSQL Regression Tests Against Existing Installation (Sequential)

Source: https://www.postgresql.org/docs/current/regress-run.html

This command runs the regression tests against an already installed and running PostgreSQL server in sequential mode. Ensure a data directory is initialized and the server is started before execution.

```bash
make installcheck
```

--------------------------------

### Set up PostgreSQL Tutorial Files

Source: https://www.postgresql.org/docs/current/tutorial-sql-intro.html

Navigate to the PostgreSQL source tutorial directory and compile the necessary C files for user-defined functions and types.

```bash
$ **cd _..._/src/tutorial**
$ **make**
```

--------------------------------

### Multiple Connections Example Output

Source: https://www.postgresql.org/docs/current/ecpg-connect.html

Expected output from the multiple database connections example program, showing the current database for each connection query.

```text
current=testdb3 (should be testdb3)
current=testdb2 (should be testdb2)
current=testdb1 (should be testdb1)
```

--------------------------------

### Get Syntax Help for Multi-word SQL Commands with \help

Source: https://www.postgresql.org/docs/current/app-psql.htm

Illustrates how to get syntax help for SQL commands consisting of multiple words without needing to quote them.

```psql
\help alter table
```

--------------------------------

### PL/pgSQL: Get Row Count with GET DIAGNOSTICS

Source: https://www.postgresql.org/docs/current/plpgsql-statements.html

This example demonstrates how to use GET DIAGNOSTICS to retrieve the number of rows processed by the most recent SQL command into an integer variable.

```plpgsql
GET DIAGNOSTICS integer_var = ROW_COUNT;
```

--------------------------------

### Simple Bind LDAP Configuration with LDAPS URL

Source: https://www.postgresql.org/docs/current/auth-ldap.html

This example demonstrates a simple bind configuration using an LDAPS URL, which combines the server, scheme, and port into a single parameter for a more compact setup.

```PostgreSQL HBA
host ... ldap ldapurl="ldaps://ldap.example.net:49151" ldapprefix="cn=" ldapsuffix=", dc=example, dc=net"
```

--------------------------------

### Example of connecting and opening a remote cursor

Source: https://www.postgresql.org/docs/current/contrib-dblink-open.html

Demonstrates establishing a connection and opening a cursor named 'foo' for a specific query.

```sql
SELECT dblink_connect('dbname=postgres options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_open('foo', 'select proname, prosrc from pg_proc');
 dblink_open
-------------
 OK
(1 row)
```

--------------------------------

### Install new PostgreSQL binaries with custom prefix

Source: https://www.postgresql.org/docs/current/pgupgrade.html

Build and install the new PostgreSQL binaries to a custom location using the prefix variable. Use this for source installs when you want to install to a non-default directory.

```bash
make prefix=/usr/local/pgsql.new install
```

--------------------------------

### Retrieve Column Data Length with GET DESCRIPTOR (Embedded SQL)

Source: https://www.postgresql.org/docs/current/ecpg-sql-get-descriptor.html

This example shows how to get the returned octet length of a specific column (here, the first column) from a descriptor area.

```sql
EXEC SQL GET DESCRIPTOR d VALUE 1 :d_returned_octet_length = RETURNED_OCTET_LENGTH;
```

--------------------------------

### FOR Integer Range Loop Examples

Source: https://www.postgresql.org/docs/current/plpgsql-control-structures.html

Practical examples of integer FOR loops demonstrating forward iteration, REVERSE iteration, and iteration with custom step values using BY clause.

```sql
FOR i IN 1..10 LOOP
    -- i will take on the values 1,2,3,4,5,6,7,8,9,10 within the loop
END LOOP;
```

```sql
FOR i IN REVERSE 10..1 LOOP
    -- i will take on the values 10,9,8,7,6,5,4,3,2,1 within the loop
END LOOP;
```

```sql
FOR i IN REVERSE 10..1 BY 2 LOOP
    -- i will take on the values 10,8,6,4,2 within the loop
END LOOP;
```

--------------------------------

### Create table for replication example

Source: https://www.postgresql.org/docs/current/logical-replication-col-lists.html

Creates a base table with multiple columns to be used in publication and replication examples.

```SQL
/* pub # */ CREATE TABLE t1(id int, a text, b text, c text, d text, e text, PRIMARY KEY(id));
```

--------------------------------

### Compile and Link Shared Library on macOS

Source: https://www.postgresql.org/docs/current/xfunc-c.html

This example demonstrates compiling and linking a C source file into a shared library on macOS. Ensure developer tools are installed for these commands to work.

```shell
cc -c foo.c
cc -bundle -flat_namespace -undefined suppress -o foo.so foo.o
```

--------------------------------

### Example of DESCRIBE with Embedded SQL

Source: https://www.postgresql.org/docs/current/ecpg-sql-describe.html

Demonstrates how to use EXEC SQL DESCRIBE to get metadata about a prepared statement, allocate and deallocate a descriptor, and retrieve a column name.

```SQL (Embedded C/ECPG)
EXEC SQL ALLOCATE DESCRIPTOR mydesc;
EXEC SQL PREPARE stmt1 FROM :sql_stmt;
EXEC SQL DESCRIBE stmt1 INTO SQL DESCRIPTOR mydesc;
EXEC SQL GET DESCRIPTOR mydesc VALUE 1 :charvar = NAME;
EXEC SQL DEALLOCATE DESCRIPTOR mydesc;
```

--------------------------------

### Example: OPEN FOR EXECUTE with format() and USING

Source: https://www.postgresql.org/docs/current/plpgsql-cursors.html

Demonstrates opening an unbound cursor using a dynamically formatted query and passing parameters with the USING clause.

```plpgsql
OPEN curs1 FOR EXECUTE format('SELECT * FROM %I WHERE col1 = $1',tabname) USING keyvalue;
```

--------------------------------

### Install procedural language via extension

Source: https://www.postgresql.org/docs/current/sql-createlanguage.htm

Uses the CREATE EXTENSION command to install a language, which is the standard approach for extensions.

```sql
CREATE EXTENSION plsample;


```

--------------------------------

### Complete crosstab Example with Sales Data

Source: https://www.postgresql.org/docs/current/tablefunc.html

A full example demonstrating table creation, data insertion, and a `crosstab` query to pivot sales data by month.

```SQL
create table sales(year int, month int, qty int);
insert into sales values(2007, 1, 1000);
insert into sales values(2007, 2, 1500);
insert into sales values(2007, 7, 500);
insert into sales values(2007, 11, 1500);
insert into sales values(2007, 12, 2000);
insert into sales values(2008, 1, 1000);

select * from crosstab(
  'select year, month, qty from sales order by 1',
  'select m from generate_series(1,12) m'
) as (
  year int,
  "Jan" int,
  "Feb" int,
  "Mar" int,
  "Apr" int,
  "May" int,
  "Jun" int,
  "Jul" int,
  "Aug" int,
  "Sep" int,
  "Oct" int,
  "Nov" int,
  "Dec" int
);
 year | Jan  | Feb  | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov  | Dec
------+------+------+-----+-----+-----+-----+-----+-----+-----+-----+------+------
 2007 | 1000 | 1500 |     |     |     |     | 500 |     |     |     | 1500 | 2000
 2008 | 1000 |      |     |     |     |     |     |     |     |     |      |
(2 rows)
```

--------------------------------

### Create tables for replication examples

Source: https://www.postgresql.org/docs/current/logical-replication-row-filter.html

Define three base tables with primary keys to be used in publication and subscription examples.

```SQL
/* pub # */ CREATE TABLE t1(a int, b int, c text, PRIMARY KEY(a,c));
/* pub # */ CREATE TABLE t2(d int, e int, f int, PRIMARY KEY(d));
/* pub # */ CREATE TABLE t3(g int, h int, i int, PRIMARY KEY(g));
```

--------------------------------

### Configure PostgreSQL autostart on Linux via rc.local

Source: https://www.postgresql.org/docs/current/server-start.html

Append this command to /etc/rc.d/rc.local or /etc/rc.local to initiate the database on boot.

```shell
/usr/local/pgsql/bin/pg_ctl start -l logfile -D /usr/local/pgsql/data

```

--------------------------------

### Complete Embedded SQL Procedure with GET DESCRIPTOR

Source: https://www.postgresql.org/docs/current/ecpg-sql-get-descriptor.html

This comprehensive C example demonstrates the full workflow of using GET DESCRIPTOR to retrieve column count, data length, and data value after executing a SELECT statement.

```c
int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    int  d_count;
    char d_data[1024];
    int  d_returned_octet_length;
EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO testdb AS con1 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL ALLOCATE DESCRIPTOR d;

    /* Declare, open a cursor, and assign a descriptor to the cursor  */
    EXEC SQL DECLARE cur CURSOR FOR SELECT current_database();
    EXEC SQL OPEN cur;
    EXEC SQL FETCH NEXT FROM cur INTO SQL DESCRIPTOR d;

    /* Get a number of total columns */
    EXEC SQL GET DESCRIPTOR d :d_count = COUNT;
    printf("d_count                 = %d\n", d_count);

    /* Get length of a returned column */
    EXEC SQL GET DESCRIPTOR d VALUE 1 :d_returned_octet_length = RETURNED_OCTET_LENGTH;
    printf("d_returned_octet_length = %d\n", d_returned_octet_length);

    /* Fetch the returned column as a string */
    EXEC SQL GET DESCRIPTOR d VALUE 1 :d_data = DATA;
    printf("d_data                  = %s\n", d_data);

    /* Closing */
    EXEC SQL CLOSE cur;
    EXEC SQL COMMIT;

    EXEC SQL DEALLOCATE DESCRIPTOR d;
    EXEC SQL DISCONNECT ALL;

    return 0;
}
```

--------------------------------

### IMPORT FOREIGN SCHEMA - Example: Import All Tables

Source: https://www.postgresql.org/docs/current/sql-importforeignschema.html

Example demonstrating how to import all table definitions from a remote schema on a foreign server into a local schema.

```APIDOC
## Example: Import All Tables from Remote Schema

### Description
Imports all table definitions from the remote schema `foreign_films` on server `film_server`, creating foreign tables in the local schema `films`.

### Request Example
```sql
IMPORT FOREIGN SCHEMA foreign_films
    FROM SERVER film_server INTO films;
```

### Result
Creates foreign tables in the `films` schema that represent all tables and views from the `foreign_films` schema on the `film_server` foreign server.
```

--------------------------------

### BeginForeignScan FDW callback signature

Source: https://www.postgresql.org/docs/current/fdw-callbacks.html

Called during executor startup to initialize a foreign scan. Should perform setup needed before scanning but not start the actual scan; when EXEC_FLAG_EXPLAIN_ONLY is set, perform only the minimum required for ExplainForeignScan and EndForeignScan.

```C
void
BeginForeignScan(ForeignScanState *node,
                 int eflags);
```

--------------------------------

### Create tsvector trigger with INSERT and SELECT example

Source: https://www.postgresql.org/docs/current/textsearch-features.html

Complete example showing table creation, trigger setup with tsvector_update_trigger, data insertion, and querying with full-text search. The trigger automatically maintains the tsv column when title or body changes.

```sql
CREATE TABLE messages (
    title       text,
    body        text,
    tsv         tsvector
);

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
ON messages FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(tsv, 'pg_catalog.english', title, body);

INSERT INTO messages VALUES('title here', 'the body text is here');

SELECT * FROM messages;
   title    |         body          |            tsv
------------+-----------------------+----------------------------
 title here | the body text is here | 'bodi':4 'text':5 'titl':1

SELECT title, body FROM messages WHERE tsv @@ to_tsquery('title & body');
   title    |         body
------------+-----------------------
 title here | the body text is here
```

--------------------------------

### ROLLBACK TO SAVEPOINT basic example

Source: https://www.postgresql.org/docs/current/sql-rollback-to.html

Simple example showing how to undo the effects of commands executed after a savepoint was established.

```sql
ROLLBACK TO SAVEPOINT my_savepoint;
```

--------------------------------

### Install Documentation Tools on Debian using apt-get

Source: https://www.postgresql.org/docs/current/docguide-toolsets.html

Install the full set of documentation tools, including DocBook XML, XSL, libxml2-utils, xsltproc, and fop, on Debian GNU/Linux.

```bash
apt-get install docbook-xml docbook-xsl libxml2-utils xsltproc fop
```

--------------------------------

### Soundex and Difference Function Usage Examples

Source: https://www.postgresql.org/docs/current/fuzzystrmatch.html

Examples demonstrating how to use the `soundex` function to convert strings to Soundex codes and the `difference` function to compare Soundex codes, including table creation and querying.

```sql
SELECT soundex('hello world!');

SELECT soundex('Anne'), soundex('Ann'), difference('Anne', 'Ann');
SELECT soundex('Anne'), soundex('Andrew'), difference('Anne', 'Andrew');
SELECT soundex('Anne'), soundex('Margaret'), difference('Anne', 'Margaret');

CREATE TABLE s (nm text);

INSERT INTO s VALUES ('john');
INSERT INTO s VALUES ('joan');
INSERT INTO s VALUES ('wobbly');
INSERT INTO s VALUES ('jack');

SELECT * FROM s WHERE soundex(nm) = soundex('john');

SELECT * FROM s WHERE difference(s.nm, 'john') > 2;
```

--------------------------------

### CONTINUE Statement Syntax and Example

Source: https://www.postgresql.org/docs/current/plpgsql-control-structures.html

Skips the remaining statements in the current loop iteration and returns control to the loop start. It can be used conditionally with the WHEN clause.

```sql
CONTINUE [ _label_ ] [ WHEN _boolean-expression_ ];
```

```sql
LOOP
    -- some computations
    EXIT WHEN count > 100;
    CONTINUE WHEN count < 50;
    -- some computations for count IN [50 .. 100]
END LOOP;
```

--------------------------------

### Example category_sql Query

Source: https://www.postgresql.org/docs/current/tablefunc.html

Provides an example SQL query for the `category_sql` parameter, which defines the output columns.

```SQL
SELECT DISTINCT cat FROM foo ORDER BY 1;
    cat
  -------
    cat1
    cat2
    cat3
    cat4
```

--------------------------------

### Example of PostgreSQL Role Creation and Membership Granting

Source: https://www.postgresql.org/docs/current/role-membership.html

This example demonstrates creating multiple roles and granting memberships with different INHERIT and SET options. It illustrates how privilege inheritance and SET ROLE behavior are affected.

```SQL
CREATE ROLE joe LOGIN;
CREATE ROLE admin;
CREATE ROLE wheel;
CREATE ROLE island;
GRANT admin TO joe WITH INHERIT TRUE;
GRANT wheel TO admin WITH INHERIT FALSE;
GRANT island TO joe WITH INHERIT TRUE, SET FALSE;
```

--------------------------------

### PostgreSQL age Function Examples

Source: https://www.postgresql.org/docs/current/functions-datetime.html

Calculates symbolic intervals using years and months. The single-argument version uses current_date at midnight as the starting point.

```sql
age(timestamp '2001-04-10', timestamp '1957-06-13')
```

```sql
age(timestamp '1957-06-13')
```

--------------------------------

### Get Local Timestamp (SQL)

Source: https://www.postgresql.org/docs/current/functions-datetime.html

Retrieves the current date and time at the start of the current transaction without time zone information, optionally with limited precision.

```SQL
localtimestamp
```

```SQL
localtimestamp(2)
```

--------------------------------

### Querying Current Date and Time Examples

Source: https://www.postgresql.org/docs/current/functions-datetime.html

Examples of retrieving current time, date, and timestamps with varying precision and time zone settings.

```sql
SELECT CURRENT_TIME;
_Result: _14:39:53.662522-05
SELECT CURRENT_DATE;
_Result: _2019-12-23
SELECT CURRENT_TIMESTAMP;
_Result: _2019-12-23 14:39:53.662522-05
SELECT CURRENT_TIMESTAMP(2);
_Result: _2019-12-23 14:39:53.66-05
SELECT LOCALTIMESTAMP;
_Result: _2019-12-23 14:39:53.662522
```

--------------------------------

### Retrieve column type OID with SPI_gettypeid

Source: https://www.postgresql.org/docs/current/spi-spi-gettypeid.html

Use this function to get the data type OID for a specific column index. Note that column numbering starts at 1.

```C
Oid SPI_gettypeid(TupleDesc _rowdesc_, int _colnumber_)
```

--------------------------------

### Get Maximum Value with PostgreSQL MAX Aggregate

Source: https://www.postgresql.org/docs/current/tutorial-agg.html

Computes the highest value from a specified column across all rows in a table. This example finds the highest low-temperature reading.

```SQL
SELECT max(temp_lo) FROM weather;
```

--------------------------------

### libpq Basic Connection and Query Execution in C

Source: https://www.postgresql.org/docs/current/libpq-example.html

Demonstrates connecting to a PostgreSQL database, executing queries, processing results with cursors in a transaction, and proper resource cleanup. Includes error handling for connection and query failures.

```C
/*
 * src/test/examples/testlibpq.c
 *
 *
 * testlibpq.c
 *
 *      Test the C version of libpq, the PostgreSQL frontend library.
 */
#include <stdio.h>
#include <stdlib.h>
#include "libpq-fe.h"

static void
exit_nicely(PGconn *conn)
{
    PQfinish(conn);
    exit(1);
}

int
main(int argc, char **argv)
{
    const char *conninfo;
    PGconn     *conn;
    PGresult   *res;
    int         nFields;
    int         i,
                j;

    /*
     * If the user supplies a parameter on the command line, use it as the
     * conninfo string; otherwise default to setting dbname=postgres and using
     * environment variables or defaults for all other connection parameters.
     */
    if (argc > 1)
        conninfo = argv[1];
    else
        conninfo = "dbname = postgres";

    /* Make a connection to the database */
    conn = PQconnectdb(conninfo);

    /* Check to see that the backend connection was successfully made */
    if (PQstatus(conn) != CONNECTION_OK)
    {
        fprintf(stderr, "%s", PQerrorMessage(conn));
        exit_nicely(conn);
    }

    /* Set always-secure search path, so malicious users can't take control. */
    res = PQexec(conn,
                 "SELECT pg_catalog.set_config('search_path', '', false)");
    if (PQresultStatus(res) != PGRES_TUPLES_OK)
    {
        fprintf(stderr, "SET failed: %s", PQerrorMessage(conn));
        PQclear(res);
        exit_nicely(conn);
    }

    /*
     * Should PQclear PGresult whenever it is no longer needed to avoid memory
     * leaks
     */
    PQclear(res);

    /*
     * Our test case here involves using a cursor, for which we must be inside
     * a transaction block.  We could do the whole thing with a single
     * PQexec() of "select * from pg_database", but that's too trivial to make
     * a good example.
     */

    /* Start a transaction block */
    res = PQexec(conn, "BEGIN");
    if (PQresultStatus(res) != PGRES_COMMAND_OK)
    {
        fprintf(stderr, "BEGIN command failed: %s", PQerrorMessage(conn));
        PQclear(res);
        exit_nicely(conn);
    }
    PQclear(res);

    /*
     * Fetch rows from pg_database, the system catalog of databases
     */
    res = PQexec(conn, "DECLARE myportal CURSOR FOR select * from pg_database");
    if (PQresultStatus(res) != PGRES_COMMAND_OK)
    {
        fprintf(stderr, "DECLARE CURSOR failed: %s", PQerrorMessage(conn));
        PQclear(res);
        exit_nicely(conn);
    }
    PQclear(res);

    res = PQexec(conn, "FETCH ALL in myportal");
    if (PQresultStatus(res) != PGRES_TUPLES_OK)
    {
        fprintf(stderr, "FETCH ALL failed: %s", PQerrorMessage(conn));
        PQclear(res);
        exit_nicely(conn);
    }

    /* first, print out the attribute names */
    nFields = PQnfields(res);
    for (i = 0; i < nFields; i++)
        printf("%-15s", PQfname(res, i));
    printf("\n\n");

    /* next, print out the rows */
    for (i = 0; i < PQntuples(res); i++)
    {
        for (j = 0; j < nFields; j++)
            printf("%-15s", PQgetvalue(res, i, j));
        printf("\n");
    }

    PQclear(res);

    /* close the portal ... we don't bother to check for errors ... */
    res = PQexec(conn, "CLOSE myportal");
    PQclear(res);

    /* end the transaction */
    res = PQexec(conn, "END");
    PQclear(res);

    /* close the connection to the database and cleanup */
    PQfinish(conn);

    return 0;
}
```

--------------------------------

### CREATE SERVER syntax and basic example

Source: https://www.postgresql.org/docs/current/sql-createserver.html

Define a new foreign server with a foreign-data wrapper and connection options. The IF NOT EXISTS clause prevents errors if the server already exists.

```SQL
CREATE SERVER [ IF NOT EXISTS ] _server_name_ [ TYPE '_server_type_' ] [ VERSION '_server_version_' ]
    FOREIGN DATA WRAPPER _fdw_name_
    [ OPTIONS ( _option_ '_value_' [, ... ] ) ]
```

```SQL
CREATE SERVER myserver FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'foo', dbname 'foodb', port '5432');
```

--------------------------------

### Get help on SQL commands in psql

Source: https://www.postgresql.org/docs/current/tutorial-accessdb.html

Use the `\h` command within `psql` to display help information about SQL commands. Internal `psql` commands start with a backslash.

```psql
mydb=> \h
```

--------------------------------

### Example Usage of dblink_get_connections

Source: https://www.postgresql.org/docs/current/contrib-dblink-get-connections.html

This example demonstrates how to call `dblink_get_connections` to retrieve the names of all open dblink connections.

```sql
SELECT dblink_get_connections();
```

--------------------------------

### Prepare Data Directory and Initialize with initdb

Source: https://www.postgresql.org/docs/current/creating-cluster.html

This sequence of commands prepares a new directory for the PostgreSQL data, sets correct ownership, switches to the PostgreSQL user, and then initializes the database cluster.

```bash
root# mkdir /usr/local/pgsql
root# chown postgres /usr/local/pgsql
root# su postgres
postgres$ initdb -D /usr/local/pgsql/data
```

--------------------------------

### GET pg_wal_summary_contents()

Source: https://www.postgresql.org/docs/current/functions-info.html

Returns information about the contents of a single WAL summary file identified by TLI and starting and ending LSNs. Each row indicates modified blocks or truncation/creation events.

```APIDOC
## GET pg_wal_summary_contents()

### Description
Returns one information about the contents of a single WAL summary file identified by TLI and starting and ending LSNs. Each row with `is_limit_block` false indicates that the block identified by the remaining output columns was modified by at least one WAL record within the range of records summarized by this file. Each row with `is_limit_block` true indicates either that (a) the relation fork was truncated to the length given by `relblocknumber` within the relevant range of WAL records or (b) that the relation fork was created or dropped within the relevant range of WAL records; in such cases, `relblocknumber` will be zero.

### Method
GET

### Endpoint
pg_wal_summary_contents(tli, start_lsn, end_lsn)

### Parameters
#### Path Parameters
- **tli** (bigint) - Required - The Timeline ID.
- **start_lsn** (pg_lsn) - Required - The starting LSN of the WAL summary file.
- **end_lsn** (pg_lsn) - Required - The ending LSN of the WAL summary file.

### Request Example

### Response
#### Success Response (200)
- **relfilenode** (oid) - The relation filenode.
- **reltablespace** (oid) - The relation tablespace OID.
- **reldatabase** (oid) - The relation database OID.
- **relforknumber** (smallint) - The relation fork number.
- **relblocknumber** (bigint) - The relation block number.
- **is_limit_block** (boolean) - Indicates if it's a limit block (truncation/creation).

#### Response Example
```
[
  {
    "relfilenode": 16384,
    "reltablespace": 1663,
    "reldatabase": 13000,
    "relforknumber": 0,
    "relblocknumber": 10,
    "is_limit_block": false
  },
  {
    "relfilenode": 16385,
    "reltablespace": 1663,
    "reldatabase": 13000,
    "relforknumber": 0,
    "relblocknumber": 0,
    "is_limit_block": true
  }
]
```
```

--------------------------------

### Query pg_backend_memory_contexts Example

Source: https://www.postgresql.org/docs/current/view-pg-backend-memory-contexts.html

Example query demonstrating how to effectively use the pg_backend_memory_contexts view to calculate total bytes used by a specific memory context and all of its children. This example shows best practices for handling unstable path identifiers.

```APIDOC
## Example: Calculate Memory Usage for CacheMemoryContext

### Description
This example demonstrates an effective usage of the `path` column to calculate the total number of bytes used by `CacheMemoryContext` and all of its children.

### Query
```sql
WITH memory_contexts AS (
    SELECT * FROM pg_backend_memory_contexts
)
SELECT sum(c1.total_bytes)
FROM memory_contexts c1, memory_contexts c2
WHERE c2.name = 'CacheMemoryContext'
AND c1.path[c2.level] = c2.path[c2.level];
```

### Explanation
- The Common Table Expression (CTE) is used to ensure the context IDs in the `path` column match between both evaluations of the view
- The query joins the memory_contexts view with itself to find all contexts that are children of `CacheMemoryContext`
- The condition `c1.path[c2.level] = c2.path[c2.level]` ensures that contexts share the same parent at the level of `CacheMemoryContext`
- The `sum(c1.total_bytes)` aggregates the total memory allocated to `CacheMemoryContext` and all its descendants

### Result
Returns a single row with the total bytes allocated for `CacheMemoryContext` and all of its child contexts.
```

--------------------------------

### Install PostgreSQL Extension with Non-Standard Prefix

Source: https://www.postgresql.org/docs/current/extend-pgxs.html

This command installs an extension to a custom prefix. If the prefix doesn't contain 'postgres' or 'pgsql', 'postgresql' is appended to the installation paths.

```shell
make install prefix=/usr/local/extras
```

--------------------------------

### Build PostgreSQL Server and Utilities

Source: https://www.postgresql.org/docs/current/install-make.html

Use these commands to start the basic build process for PostgreSQL. This will compile the server, utilities, and client applications.

```make
make
make all
```

--------------------------------

### CLI pgbench -i

Source: https://www.postgresql.org/docs/current/pgbench.html

Initializes the database by creating and populating the necessary tables for the TPC-B-like benchmark.

```APIDOC
## CLI pgbench -i

### Description
Initializes the database by creating and populating the necessary tables (pgbench_accounts, pgbench_branches, pgbench_history, and pgbench_tellers) for the TPC-B-like benchmark.

### Method
CLI

### Endpoint
pgbench -i [option...] [dbname]

### Parameters
#### Path Parameters
- **dbname** (string) - Required - The name of the database to initialize.

#### Query Parameters
- **-s** (integer) - Optional - Scale factor to increase the number of rows.
- **-F** (integer) - Optional - Fillfactor for the created tables.
- **-h** (string) - Optional - Database server host.
- **-p** (integer) - Optional - Database server port.
- **-U** (string) - Optional - Database user name.

### Request Example
pgbench -i -s 10 mydatabase

### Response
#### Success Response (200)
- **Output** (string) - Console output indicating table creation and population.
```

--------------------------------

### Get Current Timestamp with Time Zone (SQL)

Source: https://www.postgresql.org/docs/current/functions-datetime.html

Retrieves the current date and time at the start of the current transaction, optionally with limited precision, including time zone information.

```SQL
current_timestamp
```

```SQL
current_timestamp(0)
```

--------------------------------

### SQL Extension and Server Setup

Source: https://www.postgresql.org/docs/current/file-fdw.html

Initial commands required to enable the file_fdw extension and register a foreign server to use the wrapper.

```APIDOC
## SQL SETUP

### Description
Installs the file_fdw extension and creates a foreign server object that uses the file_fdw handler.

### Method
SQL

### Endpoint
CREATE EXTENSION / CREATE SERVER

### Request Example
CREATE EXTENSION file_fdw;
CREATE SERVER pglog FOREIGN DATA WRAPPER file_fdw;

### Response
#### Success Response (200)
- **status** (string) - CREATE SERVER
```

--------------------------------

### SELECT pg_backup_start(text, boolean)

Source: https://www.postgresql.org/docs/current/functions-admin.html

Prepares the server to begin an on-line backup by setting a label and optionally forcing a checkpoint.

```APIDOC
## SELECT pg_backup_start(label, fast)

### Description
Prepares the server to begin an on-line backup. This function is restricted to superusers by default, but other users can be granted EXECUTE permissions.

### Method
SELECT

### Endpoint
pg_backup_start(label text, fast boolean)

### Parameters
#### Path Parameters
- **label** (text) - Required - An arbitrary user-defined label for the backup (e.g., the name of the backup dump file).
- **fast** (boolean) - Optional - If true, specifies executing pg_backup_start as quickly as possible by forcing an immediate checkpoint.

### Request Example
SELECT pg_backup_start('daily_backup', true);

### Response
#### Success Response (200)
- **pg_lsn** (pg_lsn) - The starting write-ahead log location for the backup.

#### Response Example
"0/16000000"
```

--------------------------------

### Example of a Poorly Structured PostgreSQL Error Message

Source: https://www.postgresql.org/docs/current/error-style-guide.html

This snippet illustrates an error message that combines implementation details and hints into a single, unformatted line, which is discouraged by the style guide.

```text
IpcMemoryCreate: shmget(key=%d, size=%u, 0%o) failed: %m
(plus a long addendum that is basically a hint)
```

--------------------------------

### CREATE USER MAPPING example with credentials

Source: https://www.postgresql.org/docs/current/sql-createusermapping.html

Creates a user mapping for user 'bob' on server 'foo' with authentication credentials. The OPTIONS clause specifies the actual username and password for the foreign server connection.

```sql
CREATE USER MAPPING FOR bob SERVER foo OPTIONS (user 'bob', password 'secret');
```

--------------------------------

### COMMIT Simple Example

Source: https://www.postgresql.org/docs/current/sql-commit.htm

Basic example of committing the current transaction to make all changes permanent.

```sql
COMMIT;
```

--------------------------------

### Install PostgreSQL Extension with Specific Prefix

Source: https://www.postgresql.org/docs/current/extend-pgxs.html

Use this command to install an extension to a custom directory prefix, such as '/usr/local/postgresql'.

```shell
make install prefix=/usr/local/postgresql
```

--------------------------------

### ArchiveStartupCB Callback

Source: https://www.postgresql.org/docs/current/archive-module-callbacks.html

The `startup_cb` callback is invoked when the archive module is loaded, allowing for initial setup and state management.

```APIDOC
## ArchiveStartupCB Callback

### Description
The `startup_cb` callback is called shortly after the module is loaded. This callback can be used to perform any additional initialization required. If the archive module has any state, it can use `state->private_data` to store it.

### Parameters
- **state** (ArchiveModuleState *) - Pointer to the module's state structure.

### Return Value
- **void** - This callback does not return a value.
```

--------------------------------

### Complex annotated lquery example

Source: https://www.postgresql.org/docs/current/ltree.html

This example demonstrates combining prefixes, quantifiers, case-insensitivity, and logical NOT in a single path query.

```sql
Top.*{0,2}.sport*@.!football|tennis{1,}.Russ*|Spain
a.  b.     c.      d.                   e.
```

--------------------------------

### Define Composite Type and Table in SQL

Source: https://www.postgresql.org/docs/current/ecpg-variables.html

This SQL snippet defines a composite type 'comp_t' and a table 't4' that uses it, then inserts sample data. This setup is used for subsequent ECPG examples.

```sql
CREATE TYPE comp_t AS (intval integer, textval varchar(32));
CREATE TABLE t4 (compval comp_t);
INSERT INTO t4 VALUES ( (256, 'PostgreSQL') );
```

--------------------------------

### CONNECT Command Syntax

Source: https://www.postgresql.org/docs/current/ecpg-sql-connect.html

Illustrates the general syntax for the `CONNECT` command, including options for specifying connection targets, names, and user credentials.

```sql
CONNECT TO _connection_target_ [ AS _connection_name_ ] [ USER _connection_user_ ]
CONNECT TO DEFAULT
CONNECT _connection_user_
DATABASE _connection_target_
```

--------------------------------

### FETCH Command Examples (PL/pgSQL)

Source: https://www.postgresql.org/docs/current/plpgsql-cursors.html

Demonstrates various uses of the PL/pgSQL FETCH command, including different directions and target variables.

```SQL
FETCH curs1 INTO rowvar;
```

```SQL
FETCH curs2 INTO foo, bar, baz;
```

```SQL
FETCH LAST FROM curs3 INTO x, y;
```

```SQL
FETCH RELATIVE -2 FROM curs4 INTO x;
```

--------------------------------

### Show All Configuration Parameters in PostgreSQL

Source: https://www.postgresql.org/docs/current/sql-show.htm

Lists all available run-time configuration parameters along with their current settings and descriptions.

```sql
SHOW ALL;
            name         | setting |                description
-------------------------+---------+-------------------------------------------------
 allow_system_table_mods | off     | Allows modifications of the structure of ...
    .
    .
    .
 xmloption               | content | Sets whether XML data in implicit parsing ...
 zero_damaged_pages      | off     | Continues processing past damaged page headers.
(196 rows)
```

--------------------------------

### Build HTML documentation using Make

Source: https://www.postgresql.org/docs/current/docguide-build.html

Run these commands in the doc/src/sgml directory. The website style option requires network access to fetch external stylesheets.

```shell
doc/src/sgml$ **make html**

```

```shell
doc/src/sgml$ **make STYLE=website html**

```

--------------------------------

### Install Documentation Tools on macOS using Homebrew

Source: https://www.postgresql.org/docs/current/docguide-toolsets.html

This command installs the necessary DocBook, XSL, libxslt, and FOP packages on macOS via Homebrew.

```bash
brew install docbook docbook-xsl libxslt fop
```

--------------------------------

### Get Single WAL Record Information in PostgreSQL

Source: https://www.postgresql.org/docs/current/pgwalinspect.html

Use this function to retrieve detailed information for a specific WAL record identified by its LSN. If the provided LSN is not at the start of a record, it returns information for the next valid record.

```sql
postgres=# SELECT * FROM pg_get_wal_record_info('0/E419E28');
-[ RECORD 1 ]----+-------------------------------------------------
start_lsn        | 0/E419E28
end_lsn          | 0/E419E68
prev_lsn         | 0/E419D78
xid              | 0
resource_manager | Heap2
record_type      | VACUUM
record_length    | 58
main_data_length | 2
fpi_length       | 0
description      | nunused: 5, unused: [1, 2, 3, 4, 5]
block_ref        | blkref #0: rel 1663/16385/1249 fork main blk 364
```

--------------------------------

### Populate unit, shoe_data, and shoelace_data tables

Source: https://www.postgresql.org/docs/current/rules-views.html

Insert sample data into the unit, shoe_data, and shoelace_data tables to demonstrate view queries. This setup is required before running SELECT queries on the views.

```SQL
INSERT INTO unit VALUES ('cm', 1.0);
INSERT INTO unit VALUES ('m', 100.0);
INSERT INTO unit VALUES ('inch', 2.54);

INSERT INTO shoe_data VALUES ('sh1', 2, 'black', 70.0, 90.0, 'cm');
INSERT INTO shoe_data VALUES ('sh2', 0, 'black', 30.0, 40.0, 'inch');
INSERT INTO shoe_data VALUES ('sh3', 4, 'brown', 50.0, 65.0, 'cm');
INSERT INTO shoe_data VALUES ('sh4', 3, 'brown', 40.0, 50.0, 'inch');

INSERT INTO shoelace_data VALUES ('sl1', 5, 'black', 80.0, 'cm');
INSERT INTO shoelace_data VALUES ('sl2', 6, 'black', 100.0, 'cm');
INSERT INTO shoelace_data VALUES ('sl3', 0, 'black', 35.0 , 'inch');
INSERT INTO shoelace_data VALUES ('sl4', 8, 'black', 40.0 , 'inch');
INSERT INTO shoelace_data VALUES ('sl5', 4, 'brown', 1.0 , 'm');
INSERT INTO shoelace_data VALUES ('sl6', 0, 'brown', 0.9 , 'm');
INSERT INTO shoelace_data VALUES ('sl7', 7, 'brown', 60 , 'cm');
INSERT INTO shoelace_data VALUES ('sl8', 1, 'brown', 40 , 'inch');
```

--------------------------------

### PQparamtype - Get Prepared Statement Parameter Data Type

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Returns the data type (OID) of the indicated statement parameter. Parameter numbers start at 0. This function is only useful when inspecting the result of PQdescribePrepared. For other types of results, it returns zero.

```APIDOC
## PQparamtype

### Description
Returns the data type of the indicated statement parameter. Parameter numbers start at 0.

### Signature
```c
Oid PQparamtype(const PGresult *res, int param_number);
```

### Parameters
#### Function Parameters
- **res** (const PGresult *) - Required - The query result object
- **param_number** (int) - Required - Zero-based parameter index

### Return Value
- **Oid** - The OID (Object Identifier) of the parameter's data type

### Notes
- This function is only useful when inspecting the result of PQdescribePrepared
- For other types of results, it will return zero
```

--------------------------------

### Complete SQLDA example program

Source: https://www.postgresql.org/docs/current/ecpg-descriptors.html

Full working example program demonstrating the complete SQLDA workflow: includes, error handling, connection, query preparation, parameter binding, cursor operations, and result processing.

```C
#include <stdlib.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

EXEC SQL include sqlda.h;

sqlda_t *sqlda1; /* descriptor for output */
sqlda_t *sqlda2; /* descriptor for input */

EXEC SQL WHENEVER NOT FOUND DO BREAK;
EXEC SQL WHENEVER SQLERROR STOP;

int
main(void)
{
    EXEC SQL BEGIN DECLARE SECTION;
    char query[1024] = "SELECT d.oid,* FROM pg_database d, pg_stat_database s WHERE d.oid=s.datid AND ( d.datname=? OR d.oid=? )";

    int intval;
    unsigned long long int longlongval;
    EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO uptimedb AS con1 USER uptime;
```

--------------------------------

### Allow Connections to Databases Matching Regex

Source: https://www.postgresql.org/docs/current/auth-pg-hba-conf.html

This example uses a regular expression for the DATABASE field to allow connections to databases whose names start with 'db' and end with two to four digits. It uses 'trust' authentication for connections from localhost.

```postgresql
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    "/^db\d{2,4}$/"  all             localhost               trust
```

--------------------------------

### Set-Returning Function Returning Composite Type in C

Source: https://www.postgresql.org/docs/current/xfunc-c.html

Complete working example of an SRF that returns a composite type with three integer fields. Demonstrates tuple descriptor setup, attribute metadata initialization, and tuple construction from C strings.

```C
PG_FUNCTION_INFO_V1(retcomposite);

Datum
retcomposite(PG_FUNCTION_ARGS)
{
    FuncCallContext     *funcctx;
    int                  call_cntr;
    int                  max_calls;
    TupleDesc            tupdesc;
    AttInMetadata       *attinmeta;

    /* stuff done only on the first call of the function */
    if (SRF_IS_FIRSTCALL())
    {
        MemoryContext   oldcontext;

        /* create a function context for cross-call persistence */
        funcctx = SRF_FIRSTCALL_INIT();

        /* switch to memory context appropriate for multiple function calls */
        oldcontext = MemoryContextSwitchTo(funcctx->multi_call_memory_ctx);

        /* total number of tuples to be returned */
        funcctx->max_calls = PG_GETARG_INT32(0);

        /* Build a tuple descriptor for our result type */
        if (get_call_result_type(fcinfo, NULL, &tupdesc) != TYPEFUNC_COMPOSITE)
            ereport(ERROR,
                    (errcode(ERRCODE_FEATURE_NOT_SUPPORTED),
                     errmsg("function returning record called in context "
                            "that cannot accept type record")));

        /*
         * generate attribute metadata needed later to produce tuples from raw
         * C strings
         */
        attinmeta = TupleDescGetAttInMetadata(tupdesc);
        funcctx->attinmeta = attinmeta;

        MemoryContextSwitchTo(oldcontext);
    }

    /* stuff done on every call of the function */
    funcctx = SRF_PERCALL_SETUP();

    call_cntr = funcctx->call_cntr;
    max_calls = funcctx->max_calls;
    attinmeta = funcctx->attinmeta;

    if (call_cntr < max_calls)    /* do when there is more left to send */
    {
        char       **values;
        HeapTuple    tuple;
        Datum        result;

        /*
         * Prepare a values array for building the returned tuple.
         * This should be an array of C strings which will
         * be processed later by the type input functions.
         */
        values = (char **) palloc(3 * sizeof(char *));
        values[0] = (char *) palloc(16 * sizeof(char));
        values[1] = (char *) palloc(16 * sizeof(char));
        values[2] = (char *) palloc(16 * sizeof(char));

        snprintf(values[0], 16, "%d", 1 * PG_GETARG_INT32(1));
        snprintf(values[1], 16, "%d", 2 * PG_GETARG_INT32(1));
        snprintf(values[2], 16, "%d", 3 * PG_GETARG_INT32(1));

        /* build a tuple */
        tuple = BuildTupleFromCStrings(attinmeta, values);

        /* make the tuple into a datum */
        result = HeapTupleGetDatum(tuple);

        /* clean up (this is not really necessary) */
        pfree(values[0]);
        pfree(values[1]);
        pfree(values[2]);
        pfree(values);

        SRF_RETURN_NEXT(funcctx, result);
    }
    else    /* do when there is no more left */
    {
        SRF_RETURN_DONE(funcctx);
    }
}
```

--------------------------------

### SQL identifier handling example

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Example SQL query with aliased columns to demonstrate identifier handling.

```sql
SELECT 1 AS FOO, 2 AS "BAR";
```

--------------------------------

### Dynamic SQL Example Output

Source: https://www.postgresql.org/docs/current/ecpg-connect.html

Expected output from the dynamic SQL with connection-linked identifier example, showing the result even when the default connection differs.

```text
postgres
```

--------------------------------

### Start PostgreSQL server using pg_ctl

Source: https://www.postgresql.org/docs/current/server-start.html

The pg_ctl utility provides a simplified interface for starting and stopping the server. It handles background execution and logging via the -l option.

```shell
pg_ctl start -l logfile

```

--------------------------------

### PL/Tcl Trigger Function for Row Update Count

Source: https://www.postgresql.org/docs/current/pltcl-trigger.html

This example demonstrates how to create a PL/Tcl trigger function to track row modifications. It includes the function definition, table creation, and trigger setup to increment a counter on INSERT or UPDATE operations.

```sql
CREATE FUNCTION trigfunc_modcount() RETURNS trigger AS $$
    switch $TG_op {
        INSERT {
            set NEW($1) 0
        }
        UPDATE {
            set NEW($1) $OLD($1)
            incr NEW($1)
        }
        default {
            return OK
        }
    }
    return [array get NEW]
$$ LANGUAGE pltcl;

CREATE TABLE mytab (num integer, description text, modcnt integer);

CREATE TRIGGER trig_mytab_modcount BEFORE INSERT OR UPDATE ON mytab
    FOR EACH ROW EXECUTE FUNCTION trigfunc_modcount('modcnt');
```

--------------------------------

### pg_get_wal_record_info

Source: https://www.postgresql.org/docs/current/pgwalinspect.html

Gets WAL record information about a record that is located at or after the in_lsn argument. If in_lsn isn't at the start of a WAL record, information about the next valid WAL record is shown instead. If there is no next valid WAL record, the function raises an error.

```APIDOC
## pg_get_wal_record_info(in_lsn pg_lsn)

### Description
Gets WAL record information about a record that is located at or after the in_lsn argument. If in_lsn isn't at the start of a WAL record, information about the next valid WAL record is shown instead. If there is no next valid WAL record, the function raises an error.

### Endpoint
pg_get_wal_record_info(in_lsn pg_lsn)

### Parameters
#### Path Parameters
- No Path Parameters

#### Query Parameters
- No Query Parameters

#### Request Body
- **in_lsn** (pg_lsn) - Required - The LSN (Log Sequence Number) to start searching for a WAL record.

### Request Example
```sql
SELECT * FROM pg_get_wal_record_info('0/E419E28');
```

### Response
#### Success Response (record)
- **start_lsn** (pg_lsn) - The LSN where the WAL record starts.
- **end_lsn** (pg_lsn) - The LSN where the WAL record ends.
- **prev_lsn** (pg_lsn) - The LSN of the previous WAL record.
- **xid** (integer) - The transaction ID associated with the record.
- **resource_manager** (string) - The resource manager that generated the WAL record.
- **record_type** (string) - The type of the WAL record.
- **record_length** (integer) - The total length of the WAL record in bytes.
- **main_data_length** (integer) - The length of the main data part of the WAL record.
- **fpi_length** (integer) - The length of the Full Page Image (FPI) data.
- **description** (string) - A textual description of the WAL record's contents.
- **block_ref** (string) - Information about block references within the WAL record.

#### Response Example
```
-[ RECORD 1 ]----+-------------------------------------------------
start_lsn        | 0/E419E28
end_lsn          | 0/E419E68
prev_lsn         | 0/E419D78
xid              | 0
resource_manager | Heap2
record_type      | VACUUM
record_length    | 58
main_data_length | 2
fpi_length       | 0
description      | nunused: 5, unused: [1, 2, 3, 4, 5]
block_ref        | blkref #0: rel 1663/16385/1249 fork main blk 364
```
```

--------------------------------

### PQgetlength - Get Field Data Length

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Returns the actual length of a field value in bytes. For text data format, this is equivalent to strlen(). For binary format, this provides essential information about the data size. Row and column numbers start at 0.

```APIDOC
## PQgetlength

### Description
Returns the actual length of a field value in bytes. Row and column numbers start at 0.

### Signature
```c
int PQgetlength(const PGresult *res,
                int row_number,
                int column_number);
```

### Parameters
#### Function Parameters
- **res** (const PGresult *) - Required - The query result object
- **row_number** (int) - Required - Zero-based row index
- **column_number** (int) - Required - Zero-based column index

### Return Value
- **int** - The actual data length in bytes

### Notes
- For text data format, this is the same as strlen()
- For binary format, this is essential information about the data size
- Do not rely on PQfsize to obtain the actual data length
```

--------------------------------

### Manage Large Objects using libpq in C

Source: https://www.postgresql.org/docs/current/lo-examplesect.html

Complete example showing how to import, export, and manipulate large objects. Includes functions for file I/O and seeking within a large object.

```c
/*-----------------------------------------------------------------
 *
 * testlo.c
 *    test using large objects with libpq
 *
 * Portions Copyright (c) 1996-2025, PostgreSQL Global Development Group
 * Portions Copyright (c) 1994, Regents of the University of California
 *
 *
 * IDENTIFICATION
 *    src/test/examples/testlo.c
 *
 *-----------------------------------------------------------------
 */
#include <stdio.h>
#include <stdlib.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#include "libpq-fe.h"
#include "libpq/libpq-fs.h"

#define BUFSIZE         1024

/*
 * importFile -
 *    import file "in_filename" into database as large object "lobjOid"
 *
 */
static Oid
importFile(PGconn *conn, char *filename)
{
    Oid         lobjId;
    int         lobj_fd;
    char        buf[BUFSIZE];
    int         nbytes,
                tmp;
    int         fd;

    /*
     * open the file to be read in
     */
    fd = open(filename, O_RDONLY, 0666);
    if (fd < 0)
    {
        fprintf(stderr, "cannot open unix file\"%s\"\n", filename);
    }

    /*
     * create the large object
     */
    lobjId = lo_creat(conn, INV_READ | INV_WRITE);
    if (lobjId == 0)
        fprintf(stderr, "cannot create large object");

    lobj_fd = lo_open(conn, lobjId, INV_WRITE);

    /*
     * read in from the Unix file and write to the inversion file
     */
    while ((nbytes = read(fd, buf, BUFSIZE)) > 0)
    {
        tmp = lo_write(conn, lobj_fd, buf, nbytes);
        if (tmp < nbytes)
            fprintf(stderr, "error while reading \"%s\"", filename);
    }

    close(fd);
    lo_close(conn, lobj_fd);

    return lobjId;
}

static void
pickout(PGconn *conn, Oid lobjId, int start, int len)
{
    int         lobj_fd;
    char       *buf;
    int         nbytes;
    int         nread;

    lobj_fd = lo_open(conn, lobjId, INV_READ);
    if (lobj_fd < 0)
        fprintf(stderr, "cannot open large object %u", lobjId);

    lo_lseek(conn, lobj_fd, start, SEEK_SET);
    buf = malloc(len + 1);

    nread = 0;
    while (len - nread > 0)
    {
        nbytes = lo_read(conn, lobj_fd, buf, len - nread);
        buf[nbytes] = '\0';
        fprintf(stderr, ">>> %s", buf);
        nread += nbytes;
        if (nbytes <= 0)
            break;              /* no more data? */
    }
    free(buf);
    fprintf(stderr, "\n");
    lo_close(conn, lobj_fd);
}

static void
overwrite(PGconn *conn, Oid lobjId, int start, int len)
{
    int         lobj_fd;
    char       *buf;
    int         nbytes;
    int         nwritten;
    int         i;

    lobj_fd = lo_open(conn, lobjId, INV_WRITE);
    if (lobj_fd < 0)
        fprintf(stderr, "cannot open large object %u", lobjId);

    lo_lseek(conn, lobj_fd, start, SEEK_SET);
    buf = malloc(len + 1);

    for (i = 0; i < len; i++)
        buf[i] = 'X';
    buf[i] = '\0';

    nwritten = 0;
    while (len - nwritten > 0)
    {
        nbytes = lo_write(conn, lobj_fd, buf + nwritten, len - nwritten);
        nwritten += nbytes;
        if (nbytes <= 0)
        {
            fprintf(stderr, "\nWRITE FAILED!\n");
            break;
        }
    }
    free(buf);
    fprintf(stderr, "\n");
    lo_close(conn, lobj_fd);
}


/*
 * exportFile -
 *    export large object "lobjOid" to file "out_filename"
 *
 */
static void
exportFile(PGconn *conn, Oid lobjId, char *filename)
{
    int         lobj_fd;
    char        buf[BUFSIZE];
    int         nbytes,
                tmp;
    int         fd;

    /*
     * open the large object
     */
    lobj_fd = lo_open(conn, lobjId, INV_READ);
    if (lobj_fd < 0)
        fprintf(stderr, "cannot open large object %u", lobjId);

    /*
     * open the file to be written to
     */
    fd = open(filename, O_CREAT | O_WRONLY | O_TRUNC, 0666);
    if (fd < 0)
    {
        fprintf(stderr, "cannot open unix file\"%s\"",
                filename);
    }

    /*
     * read in from the inversion file and write to the Unix file
     */
    while ((nbytes = lo_read(conn, lobj_fd, buf, BUFSIZE)) > 0)
    {
        tmp = write(fd, buf, nbytes);
        if (tmp < nbytes)
        {
            fprintf(stderr, "error while writing \"%s\"",
                    filename);
        }
    }

    lo_close(conn, lobj_fd);
    close(fd);
}

static void
exit_nicely(PGconn *conn)
{
    PQfinish(conn);
    exit(1);
}

int
main(int argc, char **argv)
{
    char       *in_filename,
               *out_filename;
    char       *database;
    Oid         lobjOid;
    PGconn     *conn;
    PGresult   *res;
```

--------------------------------

### PostgreSQL xmlroot Example

Source: https://www.postgresql.org/docs/current/functions-xml.html

Demonstrates how to use `xmlroot` to change the XML version and set the standalone declaration to 'yes'.

```sql
SELECT xmlroot(xmlparse(document '<?xml version="1.1"?><content>abc</content>'),
               version '1.0', standalone yes);
```

--------------------------------

### C Example: PostgreSQL Asynchronous Notifications with libpq

Source: https://www.postgresql.org/docs/current/libpq-example.html

This snippet demonstrates how to establish a PostgreSQL connection, set the search path, issue a LISTEN command for asynchronous notifications, and then use select() and PQnotifies() to process incoming notifications. It shows a basic event loop for handling database events.

```C
    if (argc > 1)
        conninfo = argv[1];
    else
        conninfo = "dbname = postgres";

    /* Make a connection to the database */
    conn = PQconnectdb(conninfo);

    /* Check to see that the backend connection was successfully made */
    if (PQstatus(conn) != CONNECTION_OK)
    {
        fprintf(stderr, "%s", PQerrorMessage(conn));
        exit_nicely(conn);
    }

    /* Set always-secure search path, so malicious users can't take control. */
    res = PQexec(conn,
                 "SELECT pg_catalog.set_config('search_path', '', false)");
    if (PQresultStatus(res) != PGRES_TUPLES_OK)
    {
        fprintf(stderr, "SET failed: %s", PQerrorMessage(conn));
        PQclear(res);
        exit_nicely(conn);
    }

    /*
     * Should PQclear PGresult whenever it is no longer needed to avoid memory
     * leaks
     */
    PQclear(res);

    /*
     * Issue LISTEN command to enable notifications from the rule's NOTIFY.
     */
    res = PQexec(conn, "LISTEN TBL2");
    if (PQresultStatus(res) != PGRES_COMMAND_OK)
    {
        fprintf(stderr, "LISTEN command failed: %s", PQerrorMessage(conn));
        PQclear(res);
        exit_nicely(conn);
    }
    PQclear(res);

    /* Quit after four notifies are received. */
    nnotifies = 0;
    while (nnotifies < 4)
    {
        /*
         * Sleep until something happens on the connection.  We use select(2)
         * to wait for input, but you could also use poll() or similar
         * facilities.
         */
        int         sock;
        fd_set      input_mask;

        sock = PQsocket(conn);

        if (sock < 0)
            break;              /* shouldn't happen */

        FD_ZERO(&input_mask);
        FD_SET(sock, &input_mask);

        if (select(sock + 1, &input_mask, NULL, NULL, NULL) < 0)
        {
            fprintf(stderr, "select() failed: %s\n", strerror(errno));
            exit_nicely(conn);
        }

        /* Now check for input */
        PQconsumeInput(conn);
        while ((notify = PQnotifies(conn)) != NULL)
        {
            fprintf(stderr,
                    "ASYNC NOTIFY of '%s' received from backend PID %d\n",
                    notify->relname, notify->be_pid);
            PQfreemem(notify);
            nnotifies++;
            PQconsumeInput(conn);
        }
    }

    fprintf(stderr, "Done.\n");

    /* close the connection to the database and cleanup */
    PQfinish(conn);

    return 0;
}
```

--------------------------------

### Stream Logical Changes with pg_recvlogical

Source: https://www.postgresql.org/docs/current/logicaldecoding-example.html

This example shows how to use the 'pg_recvlogical' utility to stream logical changes from a PostgreSQL database. It covers creating a slot, starting the stream, and observing DML operations. Requires client authentication for replication connections and sufficient 'max_wal_senders'.

```Bash
Example 1:
$ pg_recvlogical -d postgres --slot=test --create-slot
$ pg_recvlogical -d postgres --slot=test --start -f -
**Control**+**Z**
$ psql -d postgres -c "INSERT INTO data(data) VALUES('4');"
$ fg
BEGIN 693
table public.data: INSERT: id[integer]:4 data[text]:'4'
COMMIT 693
**Control**+**C**
```

--------------------------------

### Set Editor Line Number Arguments

Source: https://www.postgresql.org/docs/current/app-psql.htm

Configure PSQL_EDITOR_LINENUMBER_ARG to specify how the editor receives starting line numbers when using \e, \ef, or \ev commands with line arguments. Examples show plus-sign format for vi/Emacs and --line format for other editors.

```bash
PSQL_EDITOR_LINENUMBER_ARG='+'
```

```bash
PSQL_EDITOR_LINENUMBER_ARG='--line '
```

--------------------------------

### GET enum_range (anyenum, anyenum)

Source: https://www.postgresql.org/docs/current/functions-enum.html

Returns the range between two given enum values, as an ordered array. The values must be from the same enum type. If the first parameter is null, the result will start with the first value of the enum type. If the second parameter is null, the result will end with the last value of the enum type.

```APIDOC
## GET enum_range (anyenum, anyenum)

### Description
This function returns a range of values between two specified enum values, inclusive, as an ordered array. Both values must belong to the same enum type. If the first value is NULL, the range starts from the enum type's first value. If the second value is NULL, the range extends to the enum type's last value.

### Method
N/A (SQL Function)

### Endpoint
N/A (SQL Function)

### Parameters
#### Request Body
- **start_value** (anyenum) - Optional - The starting enum value for the range. Can be NULL to start from the first enum value.
- **end_value** (anyenum) - Optional - The ending enum value for the range. Can be NULL to end at the last enum value.

### Request Example
N/A

### Response
#### Success Response (200)
- **result** (anyarray) - An ordered array containing the enum values within the specified range.

#### Response Example
```
enum_range('orange'::rainbow, 'green'::rainbow) → {orange,yellow,green}
enum_range(NULL, 'green'::rainbow) → {red,orange,yellow,green}
enum_range('orange'::rainbow, NULL) → {orange,yellow,green,blue,purple}
```
```

--------------------------------

### Version-1 Function Declaration and Macro Setup

Source: https://www.postgresql.org/docs/current/xfunc-c.html

Demonstrates the basic structure required for version-1 functions, including the function signature and mandatory PG_FUNCTION_INFO_V1 macro declaration. This setup is required for all dynamically-loaded functions using the version-1 convention.

```APIDOC
## Version-1 Function Declaration

### Description
Defines the basic structure and macros required for version-1 calling convention functions in PostgreSQL.

### Function Signature
```c
Datum funcname(PG_FUNCTION_ARGS)
```

### Required Macro
```c
PG_FUNCTION_INFO_V1(funcname);
```

### Details
- The function must return type `Datum`
- The function must accept `PG_FUNCTION_ARGS` as its parameter
- The `PG_FUNCTION_INFO_V1` macro must appear in the same source file, typically just before the function definition
- This macro is required for dynamically-loaded functions
- Internal-language functions do not require this macro as PostgreSQL assumes all internal functions use version-1 convention

### Notes
- The macro call registers the function with PostgreSQL's function manager
- Without this macro, dynamically-loaded functions will not be recognized as version-1 functions
```

--------------------------------

### Install Documentation Tools on Fedora/RHEL using yum

Source: https://www.postgresql.org/docs/current/docguide-toolsets.html

Use this command to install the necessary DocBook DTDs, XSL stylesheets, and processing tools on Fedora, RHEL, and their derivatives.

```bash
yum install docbook-dtds docbook-style-xsl libxslt fop
```

--------------------------------

### StartupMessage

Source: https://www.postgresql.org/docs/current/protocol-message-formats.html

Initiates a connection to the PostgreSQL server, specifying protocol version and connection parameters.

```APIDOC
## StartupMessage

### Description
Initiates a connection to the PostgreSQL server. It includes the protocol version and a set of parameter-value pairs.

### Method
N/A (This is a protocol message, not an HTTP request)

### Endpoint
N/A

### Parameters
#### Request Body
- **Length** (Int32) - Length of message contents in bytes, including self.
- **ProtocolVersion** (Int32) - The protocol version number (e.g., 3.2 is represented as 196610).
- **Parameters** (String pairs) - A list of null-terminated parameter name and value strings. 'user' is required. Optional parameters include 'database' and 'options'. A zero byte terminates the list.

### Request Example
```
{
  "Length": 30,
  "ProtocolVersion": 196610,
  "Parameters": [
    {"name": "user", "value": "postgres"},
    {"name": "database", "value": "mydatabase"},
    {"name": "options", "value": "-c search_path=myschema"}
  ]
}
```

### Response
#### Success Response (Connection established)
- **Connection established** - Server responds with a ReadyForQuery message after successful startup.

#### Response Example
N/A (This is a protocol message, not a typical HTTP response)
```

--------------------------------

### Ranking Example Query

Source: https://www.postgresql.org/docs/current/textsearch-controls.html

An example SQL query demonstrating how to use ts_rank_cd to find and order the top ten highest-ranked search results.

```APIDOC
## Ranking Search Results Example

### Description
This example demonstrates how to select the ten highest-ranked matches using the `ts_rank_cd` function, ordering them by rank in descending order.

### Method
SQL Query

### Endpoint
N/A (SQL Query)

### Parameters
- **weights** (float4[]) - Optional - Default: `{0.1, 0.2, 0.4, 1.0}`. Used by `ts_rank_cd` to weigh word categories.
- **normalization** (integer) - Optional - Default: `0`. Controls document length impact on rank.

### Request Example
```sql
SELECT title, ts_rank_cd(textsearch, query) AS rank
FROM apod, to_tsquery('neutrino|(dark & matter)') query
WHERE query @@ textsearch
ORDER BY rank DESC
LIMIT 10;
```

### Response
#### Success Response (Table)
- **title** (text) - The title of the document.
- **rank** (float4) - The calculated rank of the document.

#### Response Example
```
                     title                     |   rank
-----------------------------------------------+----------
 Neutrinos in the Sun                          |      3.1
 The Sudbury Neutrino Detector                 |      2.4
 A MACHO View of Galactic Dark Matter          |  2.01317
 Hot Gas and Dark Matter                       |  1.91171
 The Virgo Cluster: Hot Plasma and Dark Matter |  1.90953
 Rafting for Solar Neutrinos                   |      1.9
 NGC 4650A: Strange Galaxy and Dark Matter     |  1.85774
 Hot Gas and Dark Matter                       |   1.6123
 Ice Fishing for Cosmic Neutrinos              |      1.6
 Weak Lensing Distorts the Universe            | 0.818218
```
```

--------------------------------

### CREATE TABLESPACE basic example

Source: https://www.postgresql.org/docs/current/sql-createtablespace.html

Create a tablespace named dbspace at the specified file system location after the directory has been prepared.

```sql
CREATE TABLESPACE dbspace LOCATION '/data/dbs';
```

--------------------------------

### PostgreSQL hstore Text Input Examples

Source: https://www.postgresql.org/docs/current/hstore.html

Examples of hstore text input format, showing simple key-value pairs and those requiring quoting for special characters. The order of pairs is not significant.

```sql
k => v
foo => bar, baz => whatever
"1-a" => "anything at all"
```

--------------------------------

### Makefile for PostgreSQL Extension Installation

Source: https://www.postgresql.org/docs/current/extend-extensions.html

Provides a basic Makefile using PGXS to automate the installation of the 'pair' extension's control and SQL script files into the correct PostgreSQL directory.

```makefile
EXTENSION = pair
DATA = pair--1.0.sql

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)
```

--------------------------------

### DROP TABLE Example — Remove Multiple Tables

Source: https://www.postgresql.org/docs/current/sql-droptable.htm

Example showing how to drop two tables (films and distributors) in a single command.

```SQL
DROP TABLE films, distributors;
```

--------------------------------

### Build HTML Documentation with Meson

Source: https://www.postgresql.org/docs/current/docguide-build-meson.html

Run this command from the build directory to generate the HTML version of PostgreSQL documentation. Output is placed in build/doc/src/sgml.

```bash
build$ ninja html
```

--------------------------------

### Create and Populate connectby Example Table

Source: https://www.postgresql.org/docs/current/tablefunc.html

DDL and DML statements to create a sample hierarchical tree table and insert test data with parent-key relationships for use with connectby examples.

```SQL
CREATE TABLE connectby_tree(keyid text, parent_keyid text, pos int);

INSERT INTO connectby_tree VALUES('row1',NULL, 0);
INSERT INTO connectby_tree VALUES('row2','row1', 0);
INSERT INTO connectby_tree VALUES('row3','row1', 0);
INSERT INTO connectby_tree VALUES('row4','row2', 1);
INSERT INTO connectby_tree VALUES('row5','row2', 0);
INSERT INTO connectby_tree VALUES('row6','row4', 0);
INSERT INTO connectby_tree VALUES('row7','row3', 0);
INSERT INTO connectby_tree VALUES('row8','row6', 0);
INSERT INTO connectby_tree VALUES('row9','row5', 0);
```

--------------------------------

### STARTUP / StartupMessage

Source: https://www.postgresql.org/docs/current/protocol-flow.html

Initiates a session by sending user and database information to the server to identify the protocol version and connection parameters.

```APIDOC
## STARTUP / StartupMessage

### Description
To begin a session, a frontend opens a connection to the server and sends a startup message identifying the user, database, and protocol version.

### Method
STARTUP

### Endpoint
/

### Parameters
#### Request Body
- **user** (string) - Required - The name of the database user the user wants to connect as.
- **database** (string) - Required - The name of the database the user wants to connect to.
- **protocol_version** (integer) - Required - Identifies the particular protocol version to be used.

### Request Example
{
  "user": "postgres",
  "database": "postgres",
  "protocol_version": 196608
}

### Response
#### Success Response (AuthenticationOk)
- **AuthenticationOk** (message) - The authentication exchange is successfully completed.

#### Error Response (ErrorResponse)
- **ErrorResponse** (message) - The connection attempt has been rejected and the server closes the connection.

#### Response Example
{
  "type": "AuthenticationOk"
}
```

--------------------------------

### ECPG COMMAND GET DESCRIPTOR

Source: https://www.postgresql.org/docs/current/ecpg.htm

Gets information from an SQL descriptor area.

```APIDOC
## ECPG COMMAND GET DESCRIPTOR

### Description
Get information from an SQL descriptor area.

### Command
GET DESCRIPTOR
```

--------------------------------

### Create hash partitioned table in PostgreSQL

Source: https://www.postgresql.org/docs/current/sql-createtable.htm

This example shows how to create a table partitioned by hash on an integer column.

```SQL
CREATE TABLE orders (
    order_id     bigint not null,
    cust_id      bigint not null,
    status       text
) PARTITION BY HASH (order_id);
```

--------------------------------

### Install Documentation Tools on macOS using MacPorts

Source: https://www.postgresql.org/docs/current/docguide-toolsets.html

Use this command with MacPorts to install the DocBook XML, XSL, libxslt, and FOP packages on macOS.

```bash
sudo port install docbook-xml docbook-xsl-nons libxslt fop
```

--------------------------------

### Example Usage of PostgreSQL repeat() Function

Source: https://www.postgresql.org/docs/current/functions.htm

This example demonstrates how to use the `repeat` function in PostgreSQL, showing its input parameters and the resulting output.

```SQL
repeat('Pg', 4) → PgPgPgPg
```

--------------------------------

### Rename Collation Example

Source: https://www.postgresql.org/docs/current/sql-altercollation.html

Example of renaming an existing collation from de_DE to german.

```SQL
ALTER COLLATION "de_DE" RENAME TO german;
```

--------------------------------

### MOVE Command Examples (PL/pgSQL)

Source: https://www.postgresql.org/docs/current/plpgsql-cursors.html

Illustrates different ways to reposition a cursor using the PL/pgSQL MOVE command.

```SQL
MOVE curs1;
```

```SQL
MOVE LAST FROM curs3;
```

```SQL
MOVE RELATIVE -2 FROM curs4;
```

```SQL
MOVE FORWARD 2 FROM curs4;
```

--------------------------------

### Connect and Identify System using psql

Source: https://www.postgresql.org/docs/current/protocol-replication.html

Demonstrates how to establish a logical replication connection using psql and execute the IDENTIFY_SYSTEM command to retrieve cluster information. This is useful for testing replication commands.

```bash
psql "dbname=postgres replication=database" -c "IDENTIFY_SYSTEM;"
```

--------------------------------

### ECPG CONNECT TO Statement Examples

Source: https://www.postgresql.org/docs/current/ecpg-connect.html

These examples demonstrate various ways to connect to a PostgreSQL database using ECPG, including direct target specification and using a named connection with user credentials.

```sql
EXEC SQL CONNECT TO mydb@sql.mydomain.com;
```

```sql
EXEC SQL CONNECT TO tcp:postgresql://sql.mydomain.com/mydb AS myconnection USER john;
```

--------------------------------

### Extract Substring by Start Position and Length in PostgreSQL

Source: https://www.postgresql.org/docs/current/functions-string.html

The `substring` function extracts a portion of a string based on a starting character position and an optional character count. At least one of `start` or `count` must be provided.

```SQL
substring('Thomas' from 2 for 3)
```

```SQL
substring('Thomas' from 3)
```

```SQL
substring('Thomas' for 2)
```

--------------------------------

### Control PostgreSQL Server Instances

Source: https://www.postgresql.org/docs/current/logical-replication-upgrade.html

Stop the existing database server and start the upgraded instance using pg_ctl.

```shell
pg_ctl -D /opt/PostgreSQL/data1 stop
```

```shell
pg_ctl -D /opt/PostgreSQL/data1_upgraded start -l logfile
```

```shell
pg_ctl -D /opt/PostgreSQL/data2 stop
```

```shell
pg_ctl -D /opt/PostgreSQL/data2_upgraded start -l logfile
```

--------------------------------

### Configure PostgreSQL for Default Installation

Source: https://www.postgresql.org/docs/current/install-make.html

Run this command to configure the PostgreSQL source tree for a default installation. It detects system variables and operating system quirks.

```shell
./configure
```

--------------------------------

### CREATE EVENT TRIGGER Example

Source: https://www.postgresql.org/docs/current/plperl-event-triggers.html

Example demonstrating how to create a PL/Perl event trigger function and associate it with a database event. This example shows a simple event trigger that logs event information using elog.

```APIDOC
## CREATE EVENT TRIGGER Example

### Description
This example illustrates creating a PL/Perl event trigger function that captures and logs event information.

### Function Definition
```sql
CREATE OR REPLACE FUNCTION perlsnitch() RETURNS event_trigger AS $$
  elog(NOTICE, "perlsnitch: " . $_TD->{event} . " " . $_TD->{tag} . " ");
$$ LANGUAGE plperl;
```

### Trigger Creation
```sql
CREATE EVENT TRIGGER perl_a_snitch
    ON ddl_command_start
    EXECUTE FUNCTION perlsnitch();
```

### Explanation
- **Function**: perlsnitch() - A PL/Perl function that logs the event name and command tag
- **Event Trigger**: perl_a_snitch - Executes the perlsnitch() function when DDL commands start
- **Event**: ddl_command_start - The trigger fires at the beginning of DDL command execution
```

--------------------------------

### Example: Create UTF8 to LATIN1 Conversion

Source: https://www.postgresql.org/docs/current/sql-createconversion.html

This example demonstrates how to create a conversion named 'myconv' from 'UTF8' to 'LATIN1' using a user-defined function 'myfunc'.

```SQL
CREATE CONVERSION myconv FOR 'UTF8' TO 'LATIN1' FROM myfunc;
```

--------------------------------

### Create Subscription on Subscriber

Source: https://www.postgresql.org/docs/current/logical-replication-quick-setup.html

Establishes a connection to the publisher and starts the initial synchronization and incremental replication.

```sql
CREATE SUBSCRIPTION mysub CONNECTION 'dbname=foo host=bar user=repuser' PUBLICATION mypub;

```

--------------------------------

### Install macOS developer tools

Source: https://www.postgresql.org/docs/current/installation-platform-notes.html

Install Apple's command line developer tools before building from source. This command triggers a GUI dialog for confirmation.

```shell
xcode-select --install


```

--------------------------------

### COMMAND START_REPLICATION

Source: https://www.postgresql.org/docs/current/protocol-replication.html

Instructs the server to begin streaming WAL (Write-Ahead Log) data from a specified WAL location, optionally using a replication slot and timeline.

```APIDOC
## COMMAND START_REPLICATION

### Description
Instructs the server to begin streaming WAL (Write-Ahead Log) data from a specified WAL location, optionally using a replication slot and timeline. If a slot is provided, it will be updated as replication progresses.

### Method
COMMAND

### Endpoint
START_REPLICATION [SLOT <slot_name>] [PHYSICAL] <XXX/XXX> [TIMELINE <tli>]

### Parameters
#### Path Parameters
- **XXX/XXX** (text) - Required - The starting WAL location (LSN) from which to begin streaming.

#### Query Parameters
- **slot_name** (text) - Optional - The name of the replication slot to be updated as replication progresses.
- **PHYSICAL** (keyword) - Optional - Specifies physical replication. (Often inferred or default).
- **tli** (int8) - Optional - The timeline ID to stream from. If not specified, the server's current timeline is selected.

### Response
#### Success Response (200)
- The server responds with a CopyBothResponse message and then streams WAL data.
- **WAL Data Format (within CopyData messages):**
  - **Byte1('w')** (byte) - Identifies the message as WAL data.
  - **Int64** (int64) - The starting point of the WAL data in this message.
  - **Int64** (int64) - The current end of WAL on the server.
  - **Int64** (int64) - The server's system clock at the time of transmission, as microseconds since midnight on 2000-01-01.
  - **Byte n** (byte array) - The actual WAL data payload.

#### End of Timeline Response (if streaming an old timeline)
- After streaming all WAL on an old timeline, the server sends a result set with:
  - **next_timeline_id** (int8) - The ID of the next timeline in the server's history.
  - **switch_wal_location** (text) - The WAL location where the timeline switch happened.
```

--------------------------------

### Create a PostgreSQL Products Table

Source: https://www.postgresql.org/docs/current/ddl-basics.html

An example of creating a table with more descriptive names and common data types like integer, text, and numeric.

```sql
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric
);
```

--------------------------------

### Change Collation Owner Example

Source: https://www.postgresql.org/docs/current/sql-altercollation.html

Example of changing the owner of the en_US collation to user joe.

```SQL
ALTER COLLATION "en_US" OWNER TO joe;
```

--------------------------------

### Move old PostgreSQL installation directory

Source: https://www.postgresql.org/docs/current/pgupgrade.html

Rename the old PostgreSQL installation directory to prevent conflicts with the new version. Use this when the installation directory is not version-specific (e.g., /usr/local/pgsql). Only necessary after shutting down the current PostgreSQL server.

```bash
mv /usr/local/pgsql /usr/local/pgsql.old
```

--------------------------------

### Start PostgreSQL in Single-User Mode

Source: https://www.postgresql.org/docs/current/app-postgres.htm

Use this command for administrative tasks or recovery when the main server cannot be started. Provide the correct path to the database directory with -D and specify the target database.

```bash
postgres --single -D /usr/local/pgsql/data _other-options_ my_database
```

--------------------------------

### unaccent() Usage Examples

Source: https://www.postgresql.org/docs/current/unaccent.html

Examples demonstrating unaccent() with explicit dictionary parameter and with default dictionary omitted.

```sql
SELECT unaccent('unaccent', 'Hôtel');
SELECT unaccent('Hôtel');
```

--------------------------------

### SET CONNECTION Usage Examples

Source: https://www.postgresql.org/docs/current/ecpg-sql-set-connection.html

Demonstrates how to use `SET CONNECTION` with both `TO` and `=` operators to switch to a named database connection.

```Embedded SQL
EXEC SQL SET CONNECTION TO con2;
```

```Embedded SQL
EXEC SQL SET CONNECTION = con1;
```

--------------------------------

### IMPORT FOREIGN SCHEMA - Example: Import Specific Tables

Source: https://www.postgresql.org/docs/current/sql-importforeignschema.html

Example demonstrating how to import only specific tables from a remote schema using the LIMIT TO clause.

```APIDOC
## Example: Import Specific Tables Using LIMIT TO

### Description
Imports only the specified tables `actors` and `directors` from the remote schema `foreign_films` on server `film_server` into the local schema `films`. Other tables in the remote schema are ignored.

### Request Example
```sql
IMPORT FOREIGN SCHEMA foreign_films LIMIT TO (actors, directors)
    FROM SERVER film_server INTO films;
```

### Result
Creates foreign tables only for `actors` and `directors` (if they exist) in the `films` schema. All other tables in the remote schema are not imported.
```

--------------------------------

### Example: Drop a PostgreSQL Role

Source: https://www.postgresql.org/docs/current/sql-droprole.html

This example demonstrates how to remove a specific role named 'jonathan' from the database.

```sql
DROP ROLE jonathan;
```

--------------------------------

### CLOSE Command Example (PL/pgSQL)

Source: https://www.postgresql.org/docs/current/plpgsql-cursors.html

An example of closing an open cursor using the PL/pgSQL CLOSE command.

```SQL
CLOSE curs1;
```

--------------------------------

### Install file_fdw extension

Source: https://www.postgresql.org/docs/current/file-fdw.html

Registers the extension in the database to enable foreign-data wrapper functionality.

```sql
CREATE EXTENSION file_fdw;


```

--------------------------------

### Embedded SQL OPEN Command Examples

Source: https://www.postgresql.org/docs/current/ecpg-sql-open.html

Illustrates practical applications of the `OPEN` command within embedded SQL, showing how to open cursors with different binding methods.

```SQL
EXEC SQL OPEN a;
EXEC SQL OPEN d USING 1, 'test';
EXEC SQL OPEN c1 USING SQL DESCRIPTOR mydesc;
EXEC SQL OPEN :curname1;
```

--------------------------------

### LDAP LDIF Entry and Query Example

Source: https://www.postgresql.org/docs/current/libpq-ldap.html

An example LDIF file defining connection parameters and the corresponding URL used to query that specific entry.

```ldif
version:1
dn:cn=mydatabase,dc=mycompany,dc=com
changetype:add
objectclass:top
objectclass:device
cn:mydatabase
description:host=dbserver.mycompany.com
description:port=5439
description:dbname=mydb
description:user=mydb_user
description:sslmode=require

```

```text
ldap://ldap.mycompany.com/dc=mycompany,dc=com?description?one?(cn=mydatabase)

```

--------------------------------

### libpq Asynchronous Notification Handling in C

Source: https://www.postgresql.org/docs/current/libpq-example.html

Demonstrates setting up asynchronous notifications with libpq, including platform-specific includes for Windows compatibility and listening for NOTIFY events from the database.

```C
/*
 * src/test/examples/testlibpq2.c
 *
 *
 * testlibpq2.c
 *      Test of the asynchronous notification interface
 *
 * Start this program, then from psql in another window do
 *   NOTIFY TBL2;
 * Repeat four times to get this program to exit.
 *
 * Or, if you want to get fancy, try this:
 * populate a database with the following commands
 * (provided in src/test/examples/testlibpq2.sql):
 *
 *   CREATE SCHEMA TESTLIBPQ2;
 *   SET search_path = TESTLIBPQ2;
 *   CREATE TABLE TBL1 (i int4);
 *   CREATE TABLE TBL2 (i int4);
 *   CREATE RULE r1 AS ON INSERT TO TBL1 DO
 *     (INSERT INTO TBL2 VALUES (new.i); NOTIFY TBL2);
 *
 * Start this program, then from psql do this four times:
 *
 *   INSERT INTO TESTLIBPQ2.TBL1 VALUES (10);
 */

#ifdef WIN32
#include <windows.h>
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/select.h>
#include <sys/time.h>
#include <sys/types.h>

#include "libpq-fe.h"

static void
exit_nicely(PGconn *conn)
{
    PQfinish(conn);
    exit(1);
}

int
main(int argc, char **argv)
{
    const char *conninfo;
    PGconn     *conn;
    PGresult   *res;
    PGnotify   *notify;
    int         nnotifies;
```

--------------------------------

### Simple CASE Expression Example

Source: https://www.postgresql.org/docs/current/functions-conditional.html

Equivalent to the general CASE example using simple syntax. The expression is computed once and compared to each WHEN value until a match is found.

```SQL
SELECT a,
       CASE a WHEN 1 THEN 'one'
              WHEN 2 THEN 'two'
              ELSE 'other'
       END
    FROM test;

 a | case
---+-------
 1 | one
 2 | two
 3 | other
```

--------------------------------

### Run PostgreSQL Contrib Module Regression Tests Before Installation

Source: https://www.postgresql.org/docs/current/contrib.html

Execute this command in a module's subdirectory to run regression tests before installing the module.

```bash
**make check**
```

--------------------------------

### Build PostgreSQL with Contrib Modules (No Documentation)

Source: https://www.postgresql.org/docs/current/install-make.html

Use this command to build everything, including `contrib` modules, but explicitly exclude the documentation. This is useful for binary-only deployments.

```make
make world-bin
```

--------------------------------

### pg_ctl start Mode

Source: https://www.postgresql.org/docs/current/app-pg-ctl.html

Launches a new PostgreSQL server in the background. The server's standard input is attached to /dev/null, and output handling can be configured with the -l option to append to a log file.

```APIDOC
## pg_ctl start

### Description
Launches a new PostgreSQL server in the background. Standard input is attached to /dev/null (or nul on Windows). Output redirection or log file configuration is recommended.

### Mode
start

### Usage
```
pg_ctl start [options]
```

### Options
- **-l logfile** - Append server output to the specified log file
- **-D datadir** - Specify the database cluster data directory

### Behavior
- Server runs in background
- On Unix-like systems: output sent to pg_ctl's stdout by default
- On Windows: output sent to terminal by default
- Output redirection or -l option is recommended to prevent terminal interference
```

--------------------------------

### PostgreSQL: TABLE Command and SELECT All

Source: https://www.postgresql.org/docs/current/sql-select.htm

These SQL snippets demonstrate two equivalent ways to select all columns and rows from a table: the concise `TABLE` command and the standard `SELECT *` syntax.

```SQL
TABLE _name_
```

```SQL
SELECT * FROM _name_
```

--------------------------------

### Example of DECLARE STATEMENT Usage

Source: https://www.postgresql.org/docs/current/ecpg-sql-declare-statement.html

This example demonstrates how to use `DECLARE STATEMENT` with `CONNECT`, `PREPARE`, `OPEN`, `FETCH`, and `CLOSE` for dynamic SQL execution on a specific connection.

```Embedded SQL
EXEC SQL CONNECT TO postgres AS con1;
EXEC SQL AT con1 DECLARE sql_stmt STATEMENT;
EXEC SQL DECLARE cursor_name CURSOR FOR sql_stmt;
EXEC SQL PREPARE sql_stmt FROM :dyn_string;
EXEC SQL OPEN cursor_name;
EXEC SQL FETCH cursor_name INTO :column1;
EXEC SQL CLOSE cursor_name;
```

--------------------------------

### Create a database using SQL or shell

Source: https://www.postgresql.org/docs/current/manage-ag-createdb.html

Basic commands to initialize a new database. The shell utility 'createdb' is a wrapper that connects to the 'postgres' database to issue the SQL command.

```sql
CREATE DATABASE _name_;


```

```shell
createdb _dbname_


```

--------------------------------

### PostgreSQL Range Literal Examples

Source: https://www.postgresql.org/docs/current/rangetypes.html

Examples of casting string literals to the int4range type with various bound configurations.

```sql
-- includes 3, does not include 7, and does include all points in between
SELECT '[3,7)'::int4range;

-- does not include either 3 or 7, but includes all points in between
SELECT '(3,7)'::int4range;

-- includes only the single point 4
SELECT '[4,4]'::int4range;

-- includes no points (and will be normalized to 'empty')
SELECT '[4,4)'::int4range;
```

--------------------------------

### Cube Union Function Basic Example

Source: https://www.postgresql.org/docs/current/cube.html

Demonstrates the basic usage of the `cube_union` function to combine two cubes.

```SQL
cube_union('(1,2)', '(3,4)')
```

--------------------------------

### Output Data to Logical Decoding Consumer (C)

Source: https://www.postgresql.org/docs/current/logicaldecoding-output-plugin.html

This example demonstrates how an output plugin writes data to the `StringInfo` output buffer, using `OutputPluginPrepareWrite` before writing and `OutputPluginWrite` after finishing.

```C
OutputPluginPrepareWrite(ctx, true);
appendStringInfo(ctx->out, "BEGIN %u", txn->xid);
OutputPluginWrite(ctx, true);
```

--------------------------------

### UPDATE WHERE CURRENT OF Example (PL/pgSQL)

Source: https://www.postgresql.org/docs/current/plpgsql-cursors.html

An example of updating a table row using the WHERE CURRENT OF clause with a cursor in PL/pgSQL.

```SQL
UPDATE foo SET dataval = myval WHERE CURRENT OF curs1;
```

--------------------------------

### Create computer and software tables

Source: https://www.postgresql.org/docs/current/rules-triggers.html

Defines the schema for the comparison examples, including indexed columns for hostname and manufacturer.

```sql
CREATE TABLE computer (
    hostname        text,    -- indexed
    manufacturer    text     -- indexed
);

CREATE TABLE software (
    software        text,    -- indexed
    hostname        text     -- indexed
);
```

--------------------------------

### DROP USER MAPPING example

Source: https://www.postgresql.org/docs/current/sql-dropusermapping.html

Example of dropping a user mapping for user 'bob' on server 'foo' with IF EXISTS clause to suppress errors if the mapping does not exist.

```sql
DROP USER MAPPING IF EXISTS FOR bob SERVER foo;
```

--------------------------------

### Define Startup Callback for PostgreSQL Output Plugins

Source: https://www.postgresql.org/docs/current/logicaldecoding-output-plugin.html

Called when a replication slot is created or starts streaming. Use this to validate options or initialize private state.

```C
typedef void (*LogicalDecodeStartupCB) (struct LogicalDecodingContext *ctx,
                                        OutputPluginOptions *options,
                                        bool is_init);
```

--------------------------------

### Start PostgreSQL Server with Custom Port

Source: https://www.postgresql.org/docs/current/app-postgres.htm

Use the -p option to specify a custom port number when starting the PostgreSQL server, overriding the default port.

```bash
postgres -p 1234
```

--------------------------------

### Install tsm_system_rows extension

Source: https://www.postgresql.org/docs/current/tsm-system-rows.html

Enables the SYSTEM_ROWS sampling method in the current database. This module is considered trusted and can be installed by non-superusers.

```sql
CREATE EXTENSION tsm_system_rows;

```

--------------------------------

### Create a database with basic options

Source: https://www.postgresql.org/docs/current/sql-createdatabase.htm

Standard database creation and specifying an owner and tablespace. Note that this command cannot be executed inside a transaction block.

```sql
CREATE DATABASE lusiadas;

```

```sql
CREATE DATABASE sales OWNER salesapp TABLESPACE salesspace;

```

--------------------------------

### Example of CALL Command

Source: https://www.postgresql.org/docs/current/sql-call.html

Demonstrates a simple invocation of a procedure named `do_db_maintenance` without any arguments.

```sql
CALL do_db_maintenance();
```

--------------------------------

### Start PostgreSQL Server with Custom Port and Options

Source: https://www.postgresql.org/docs/current/app-pg-ctl.html

Start the server on a non-default port (5433) with fsync disabled. The -o option passes arguments directly to the postgres backend.

```bash
$ pg_ctl -o "-F -p 5433" start
```

--------------------------------

### Initialize a new message catalog

Source: https://www.postgresql.org/docs/current/nls-translator.html

Run this command to create a new '.pot' template file when starting a new translation effort for a program.

```shell
make init-po
```

--------------------------------

### Configure Output Plugin Options in PostgreSQL

Source: https://www.postgresql.org/docs/current/logicaldecoding-output-plugin.html

Defines the output format and whether to receive heap rewrites. Set these fields within the startup callback.

```C
typedef struct OutputPluginOptions
{
    OutputPluginOutputType output_type;
    bool        receive_rewrites;
} OutputPluginOptions;
```

--------------------------------

### Sample Data for COPY FROM STDIN (Text)

Source: https://www.postgresql.org/docs/current/sql-copy.htm

This is an example of plain text data, with tab-separated values, suitable for importing into a table using COPY FROM STDIN.

```text
AF      AFGHANISTAN
AL      ALBANIA
DZ      ALGERIA
ZM      ZAMBIA
ZW      ZIMBABWE
```

--------------------------------

### Configure PostgreSQL autostart on Solaris

Source: https://www.postgresql.org/docs/current/server-start.html

This command should be placed in /etc/init.d/postgresql. A symbolic link in /etc/rc3.d is required to trigger execution during boot.

```shell
su - postgres -c "/usr/local/pgsql/bin/pg_ctl start -l logfile -D /usr/local/pgsql/data"

```

--------------------------------

### Trim bytes from the start of bytea in SQL

Source: https://www.postgresql.org/docs/current/functions-binarystring.html

Removes the longest string containing only bytes appearing in _bytesremoved_ from the start of _bytes_.

```SQL
ltrim('\x1234567890'::bytea, '\x9012'::bytea)
```

--------------------------------

### PostgreSQL Valid Decimal Numeric Constant Examples

Source: https://www.postgresql.org/docs/current/sql-syntax-lexical.html

Provides examples of correctly formatted decimal numeric constants in PostgreSQL.

```SQL
42
```

```SQL
3.5
```

```SQL
4.
```

```SQL
.001
```

```SQL
5e2
```

```SQL
1.925e-3
```

--------------------------------

### Example Event Trigger for Dropped Objects

Source: https://www.postgresql.org/docs/current/functions-event-triggers.html

This example demonstrates how to create an event trigger that uses `pg_event_trigger_dropped_objects` to log information about objects dropped during an `sql_drop` event.

```PL/pgSQL
CREATE FUNCTION test_event_trigger_for_drops()
        RETURNS event_trigger LANGUAGE plpgsql AS $$
DECLARE
    obj record;
BEGIN
    FOR obj IN SELECT * FROM pg_event_trigger_dropped_objects()
    LOOP
        RAISE NOTICE '% dropped object: % %.% %',
                     tg_tag,
                     obj.object_type,
                     obj.schema_name,
                     obj.object_name,
                     obj.object_identity;
    END LOOP;
END;
$$;
CREATE EVENT TRIGGER test_event_trigger_for_drops
   ON sql_drop
   EXECUTE FUNCTION test_event_trigger_for_drops();
```

--------------------------------

### Daitch-Mokotoff Soundex Function Examples

Source: https://www.postgresql.org/docs/current/fuzzystrmatch.html

Basic usage examples showing function output for various names. Results are arrays of 6-digit codes; multiple codes indicate alternative pronunciations.

```sql
SELECT daitch_mokotoff('George');
 daitch_mokotoff
-----------------
 {595000}
```

```sql
SELECT daitch_mokotoff('John');
 daitch_mokotoff
-----------------
 {160000,460000}
```

```sql
SELECT daitch_mokotoff('Bierschbach');
                      daitch_mokotoff
-----------------------------------------------------------
 {794575,794574,794750,794740,745750,745740,747500,747400}
```

```sql
SELECT daitch_mokotoff('Schwartzenegger');
 daitch_mokotoff
-----------------
 {479465}
```

--------------------------------

### Organizing PostgreSQL configuration with multiple include files

Source: https://www.postgresql.org/docs/current/config-setting.html

This example demonstrates using multiple `include` directives to logically separate configuration concerns like shared settings, memory-specific parameters, and server-specific customizations. Each file can be managed independently.

```PostgreSQL Configuration
include 'shared.conf'
include 'memory.conf'
include 'server.conf'
```

--------------------------------

### Initialize database cluster for sepgsql

Source: https://www.postgresql.org/docs/current/sepgsql.html

Configure shared_preload_libraries and run the sepgsql.sql script to set up security labels in a fresh cluster.

```shell
$ export PGDATA=/path/to/data/directory
$ initdb
$ vi $PGDATA/postgresql.conf
  change
    #shared_preload_libraries = ''                # (change requires restart)
  to
    shared_preload_libraries = 'sepgsql'          # (change requires restart)
$ for DBNAME in template0 template1 postgres; do
    postgres --single -F -c exit_on_error=true $DBNAME \
      </usr/local/pgsql/share/contrib/sepgsql.sql >/dev/null
  done

```

--------------------------------

### Keyword/Value Connection String Example

Source: https://www.postgresql.org/docs/current/libpq-connect.html

Format for specifying connection parameters as space-separated key-value pairs.

```plaintext
host=localhost port=5432 dbname=mydb connect_timeout=10
```

--------------------------------

### PostgreSQL current_logfiles Example Output

Source: https://www.postgresql.org/docs/current/runtime-config-logging.html

Example content of the current_logfiles file showing active log file locations for stderr, csvlog, and jsonlog destinations. This file is automatically created and updated by the logging collector.

```text
stderr log/postgresql.log
csvlog log/postgresql.csv
jsonlog log/postgresql.json
```

--------------------------------

### Run PostgreSQL Contrib Module Regression Tests After Installation

Source: https://www.postgresql.org/docs/current/contrib.html

Execute this command after a PostgreSQL server is running to verify the installed module.

```bash
**make installcheck**
```

--------------------------------

### Run pgbench Benchmark

Source: https://www.postgresql.org/docs/current/pgstatstatements.html

These commands initiate the pgbench utility to load data and run a benchmark on the 'bench' database. Adjust client and transaction counts as needed.

```bash
$ pgbench -i bench
```

```bash
$ pgbench -c10 -t300 bench
```

--------------------------------

### Example: Multi-Argument Variable-Length Function (concat_text)

Source: https://www.postgresql.org/docs/current/xfunc-c.html

Demonstrates a version-1 function that takes multiple text arguments. This example shows the pattern for functions with multiple parameters of variable-length types.

```APIDOC
## Multi-Argument Variable-Length Function Example

### Description
Function that concatenates two text values. Demonstrates handling multiple variable-length arguments.

### Function Name
concat_text

### Implementation
```c
PG_FUNCTION_INFO_V1(concat_text);

Datum
concat_text(PG_FUNCTION_ARGS)
{
    text  *arg1 = PG_GETARG_TEXT_PP(0);
    text  *arg2 = PG_GETARG_TEXT_PP(1);
    /* Function implementation continues... */
}
```

### Parameters
- **arg1** (text*) - Required - First text value to concatenate
- **arg2** (text*) - Required - Second text value to concatenate

### Return Value
- **text*** - Concatenated text result

### Notes
- Uses PG_GETARG_TEXT_PP to retrieve each text argument
- Argument numbering starts at 0
- Each argument is retrieved independently using its index
- Pattern can be extended to functions with more than two text arguments
```

--------------------------------

### ECPG SQLDA Usage Examples

Source: https://www.postgresql.org/docs/current/ecpg-descriptors.html

Demonstrates including the SQLDA header and using the INTO DESCRIPTOR clause with FETCH and DESCRIBE statements.

```C/ECPG
EXEC SQL include sqlda.h;
sqlda_t         *mysqlda;

EXEC SQL FETCH 3 FROM mycursor INTO DESCRIPTOR mysqlda;
```

```C/ECPG
EXEC SQL DESCRIBE prepared_statement INTO mysqlda;
```

--------------------------------

### Start Upgraded PostgreSQL Server

Source: https://www.postgresql.org/docs/current/logical-replication-upgrade.html

Launches the newly upgraded server instance. The -l flag is used to specify the location of the log file for the new instance.

```shell
pg_ctl -D /opt/PostgreSQL/data1_upgraded start -l logfile
```

```shell
pg_ctl -D /opt/PostgreSQL/data2_upgraded start -l logfile
```

```shell
pg_ctl -D /opt/PostgreSQL/data3_upgraded start -l logfile
```

--------------------------------

### String prefix matching with starts with in jsonpath

Source: https://www.postgresql.org/docs/current/functions-json.html

Test whether a string value begins with a specified substring using the starts with operator.

```SQL
jsonb_path_query('["John Smith", "Mary Stone", "Bob Johnson"]', '$[*] ? (@ starts with "John")')
```

--------------------------------

### Compare EXPLAIN plans with and without partition pruning

Source: https://www.postgresql.org/docs/current/ddl-partitioning.html

Use the EXPLAIN command to observe how the planner either scans all partitions or prunes them based on the configuration. Pruning significantly reduces query cost by limiting the scan to relevant partitions.

```sql
SET enable_partition_pruning = off;
EXPLAIN SELECT count(*) FROM measurement WHERE logdate >= DATE '2008-01-01';
                                    QUERY PLAN
-------------------------------------------------------------------​----------------
 Aggregate  (cost=188.76..188.77 rows=1 width=8)
   ->  Append  (cost=0.00..181.05 rows=3085 width=0)
         ->  Seq Scan on measurement_y2006m02  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
         ->  Seq Scan on measurement_y2006m03  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
...
         ->  Seq Scan on measurement_y2007m11  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
         ->  Seq Scan on measurement_y2007m12  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
         ->  Seq Scan on measurement_y2008m01  (cost=0.00..33.12 rows=617 width=0)
               Filter: (logdate >= '2008-01-01'::date)
```

```sql
SET enable_partition_pruning = on;
EXPLAIN SELECT count(*) FROM measurement WHERE logdate >= DATE '2008-01-01';
                                    QUERY PLAN
-------------------------------------------------------------------​----------------
 Aggregate  (cost=37.75..37.76 rows=1 width=8)
   ->  Seq Scan on measurement_y2008m01  (cost=0.00..33.12 rows=617 width=0)
         Filter: (logdate >= '2008-01-01'::date)
```

--------------------------------

### Establish New PostgreSQL Connection with \c or \connect

Source: https://www.postgresql.org/docs/current/app-psql.htm

These examples demonstrate various ways to establish a new connection to a PostgreSQL server using the \c or \connect command, including positional arguments, service files, connection strings, and parameter reuse.

```psql
=> \c mydb myuser host.dom 6432
```

```psql
=> \c service=foo
```

```psql
=> \c "host=localhost port=5432 dbname=mydb connect_timeout=10 sslmode=disable"
```

```psql
=> \c -reuse-previous=on sslmode=require    -- changes only sslmode
```

```psql
=> \c postgresql://tom@localhost/mydb?application_name=myapp
```

--------------------------------

### Defining a composite type for PL/Python examples

Source: https://www.postgresql.org/docs/current/plpython-data.html

This SQL type definition serves as the basis for examples demonstrating how to return composite results.

```sql
CREATE TYPE named_value AS (
  name   text,
  value  integer
);
```

--------------------------------

### Create and Execute Prepared INSERT Statement (PostgreSQL)

Source: https://www.postgresql.org/docs/current/sql-prepare.html

This example demonstrates how to create a prepared statement for an INSERT operation and then execute it with specific parameter values.

```sql
PREPARE fooplan (int, text, bool, numeric) AS
    INSERT INTO foo VALUES($1, $2, $3, $4);
EXECUTE fooplan(1, 'Hunter Valley', 't', 200.00);
```

--------------------------------

### Multiple Database Connections Example Program

Source: https://www.postgresql.org/docs/current/ecpg-connect.html

Complete embedded SQL program demonstrating connection management across three databases using CONNECT, AT clause, and SET CONNECTION. Shows how to query the current database and switch between connections.

```C
#include <stdio.h>

EXEC SQL BEGIN DECLARE SECTION;
    char dbname[1024];
EXEC SQL END DECLARE SECTION;

int
main()
{
    EXEC SQL CONNECT TO testdb1 AS con1 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL CONNECT TO testdb2 AS con2 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL CONNECT TO testdb3 AS con3 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    /* This query would be executed in the last opened database "testdb3". */
    EXEC SQL SELECT current_database() INTO :dbname;
    printf("current=%s (should be testdb3)\n", dbname);

    /* Using "AT" to run a query in "testdb2" */
    EXEC SQL AT con2 SELECT current_database() INTO :dbname;
    printf("current=%s (should be testdb2)\n", dbname);

    /* Switch the current connection to "testdb1". */
    EXEC SQL SET CONNECTION con1;

    EXEC SQL SELECT current_database() INTO :dbname;
    printf("current=%s (should be testdb1)\n", dbname);

    EXEC SQL DISCONNECT ALL;
    return 0;
}
```

--------------------------------

### Listen and notify sequence in psql

Source: https://www.postgresql.org/docs/current/sql-listen.htm

A practical example of registering a channel and receiving a notification within a psql session.

```sql
LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
```

--------------------------------

### PostgreSQL Catalog Data File Format Example

Source: https://www.postgresql.org/docs/current/system-catalog-initial-data.html

Example excerpt from `pg_database.dat` showing the Perl data structure syntax for catalog rows. Demonstrates metadata fields (oid, oid_symbol, descr), column key-value pairs, null values, and proper comma placement.

```Perl
[

# A comment could appear here.
{ oid => '1', oid_symbol => 'Template1DbOid',
  descr => 'database\'s default template',
  datname => 'template1', encoding => 'ENCODING',
  datlocprovider => 'LOCALE_PROVIDER', datistemplate => 't',
  datallowconn => 't', dathasloginevt => 'f', datconnlimit => '-1', datfrozenxid => '0',
  datminmxid => '1', dattablespace => 'pg_default', datcollate => 'LC_COLLATE',
  datctype => 'LC_CTYPE', datlocale => 'DATLOCALE', datacl => '_null_' },

]
```

--------------------------------

### Check if string starts with prefix using ^@ operator

Source: https://www.postgresql.org/docs/current/functions-string.html

Returns true if the first string starts with the second string; equivalent to the starts_with() function.

```SQL
'alphabet' ^@ 'alph'
```

--------------------------------

### Decode Prepared Transactions using SQL Interface

Source: https://www.postgresql.org/docs/current/logicaldecoding-example.html

This example shows how to use SQL commands to prepare, commit, and rollback two-phase transactions, and observe their logical decoding output. Requires `max_prepared_transactions` to be set and the slot created with `enable-two-phase`.

```sql
postgres=# BEGIN;
postgres=*# INSERT INTO data(data) VALUES('5');
postgres=*# PREPARE TRANSACTION 'test_prepared1';
```

```sql
postgres=# SELECT * FROM pg_logical_slot_get_changes('regression_slot', NULL, NULL);
    lsn    | xid |                          data
-----------+-----+---------------------------------------------------------
 0/1689DC0 | 529 | BEGIN 529
 0/1689DC0 | 529 | table public.data: INSERT: id[integer]:3 data[text]:'5'
 0/1689FC0 | 529 | PREPARE TRANSACTION 'test_prepared1', txid 529
(3 rows)
```

```sql
postgres=# COMMIT PREPARED 'test_prepared1';
```

```sql
postgres=# select * from pg_logical_slot_get_changes('regression_slot', NULL, NULL);
    lsn    | xid |                    data
-----------+-----+--------------------------------------------
 0/168A060 | 529 | COMMIT PREPARED 'test_prepared1', txid 529
(4 row)
```

```sql
postgres=#-- you can also rollback a prepared transaction
postgres=# BEGIN;
postgres=*# INSERT INTO data(data) VALUES('6');
postgres=*# PREPARE TRANSACTION 'test_prepared2';
```

```sql
postgres=# select * from pg_logical_slot_get_changes('regression_slot', NULL, NULL);
    lsn    | xid |                          data
-----------+-----+---------------------------------------------------------
 0/168A180 | 530 | BEGIN 530
 0/168A1E8 | 530 | table public.data: INSERT: id[integer]:4 data[text]:'6'
 0/168A430 | 530 | PREPARE TRANSACTION 'test_prepared2', txid 530
(3 rows)
```

```sql
postgres=# ROLLBACK PREPARED 'test_prepared2';
```

```sql
postgres=# select * from pg_logical_slot_get_changes('regression_slot', NULL, NULL);
    lsn    | xid |                     data
-----------+-----+----------------------------------------------
 0/168A4B8 | 530 | ROLLBACK PREPARED 'test_prepared2', txid 530
(1 row)
```

--------------------------------

### Rename Routine Example

Source: https://www.postgresql.org/docs/current/sql-alterroutine.html

Example demonstrating how to rename a routine using ALTER ROUTINE. This command works uniformly regardless of whether the routine is an aggregate function, normal function, or procedure.

```sql
ALTER ROUTINE foo(integer) RENAME TO foobar;
```

--------------------------------

### Example configure Script Tool Detection Output

Source: https://www.postgresql.org/docs/current/docguide-toolsets.html

This output from the configure script shows the successful detection of documentation processing tools like xmllint, xsltproc, fop, and dbtoepub.

```text
checking for xmllint... xmllint
checking for xsltproc... xsltproc
checking for fop... fop
checking for dbtoepub... dbtoepub
```

--------------------------------

### Start PostgreSQL Server in Background

Source: https://www.postgresql.org/docs/current/app-postgres.htm

This command starts the PostgreSQL server process in the background, redirecting output to a log file and detaching it from the terminal.

```bash
nohup postgres >logfile 2>&1 </dev/null &
```

--------------------------------

### Example Join Tree Structure

Source: https://www.postgresql.org/docs/current/geqo-pg-intro.html

Illustrates a conceptual join tree structure, which the GEQO module encodes as an integer string for optimization.

```text
   /\
  /\ 2
 /\ 3
4  1
```

--------------------------------

### PostgreSQL character Storage Type Conversion Example

Source: https://www.postgresql.org/docs/current/typeconv-query.html

This example demonstrates how PostgreSQL handles type conversion and sizing for a `character(20)` column, showing the effect of concatenation and automatic padding.

```sql
CREATE TABLE vv (v character(20));
INSERT INTO vv SELECT 'abc' || 'def';
SELECT v, octet_length(v) FROM vv;

          v           | octet_length
----------------------+--------------
 abcdef               |           20
(1 row)
```

--------------------------------

### Start backup mode with pg_backup_start

Source: https://www.postgresql.org/docs/current/continuous-archiving.html

Initiates backup mode on the server. The connection must be maintained until pg_backup_stop is called or the backup will abort. By default waits for the next checkpoint; pass fast => true to request an immediate checkpoint.

```sql
SELECT pg_backup_start(label => 'label', fast => false);
```

--------------------------------

### \dx[x+] [pattern]

Source: https://www.postgresql.org/docs/current/app-psql.htm

Lists installed extensions in the current database.

```APIDOC
## \dx[x+] [pattern]

### Description
Lists installed extensions.

### Method
META-COMMAND

### Endpoint
\dx[x+] [pattern]

### Parameters
#### Path Parameters
- **pattern** (string) - Optional - Filter extensions by name.
- **x** (modifier) - Optional - Expanded mode display.
- **+** (modifier) - Optional - List all objects belonging to each extension.
```

--------------------------------

### Run intarray Extension Benchmark

Source: https://www.postgresql.org/docs/current/intarray.html

This script provides steps to set up and run the 'intarray' benchmark test suite. It creates a test database, enables the 'intarray' extension, populates test data, and executes the benchmark.

```bash
cd .../contrib/intarray/bench
createdb TEST
psql -c "CREATE EXTENSION intarray" TEST
./create_test.pl | psql TEST
./bench.pl
```

--------------------------------

### DROP EVENT TRIGGER example

Source: https://www.postgresql.org/docs/current/sql-dropeventtrigger.html

Example of destroying an event trigger named 'snitch' using the basic DROP EVENT TRIGGER command.

```sql
DROP EVENT TRIGGER snitch;
```

--------------------------------

### START_REPLICATION LOGICAL

Source: https://www.postgresql.org/docs/current/protocol-replication.html

Instructs the server to start streaming WAL for logical replication from a specified slot and WAL location, or the slot's confirmed_flush_lsn.

```APIDOC
## START_REPLICATION LOGICAL

### Description
Instructs server to start streaming WAL for logical replication, starting at either WAL location _`XXX/XXX`_ or the slot's `confirmed_flush_lsn` (see Section 53.20), whichever is greater. This behavior makes it easier for clients to avoid updating their local LSN status when there is no data to process. However, starting at a different LSN than requested might not catch certain kinds of client errors; so the client may wish to check that `confirmed_flush_lsn` matches its expectations before issuing `START_REPLICATION`.

### Method
Command

### Endpoint
Not applicable (SQL-like command)

### Parameters
#### Path Parameters
- **slot_name** (string) - Required - The name of the slot to stream changes from. Must correspond to an existing logical replication slot created with `CREATE_REPLICATION_SLOT` in `LOGICAL` mode.
- **XXX/XXX** (string) - Required - The WAL location to begin streaming at.

#### Query Parameters
- **option_name** (string) - Optional - The name of an option passed to the slot's logical decoding output plugin. See Section 54.5 for options that are accepted by the standard (`pgoutput`) plugin.
- **option_value** (string) - Optional - Optional value, in the form of a string constant, associated with the specified option.

### Request Example
```sql
START_REPLICATION SLOT my_logical_slot LOGICAL 0/16000000 (include_timestamp 'true', binary 'false')
```

### Response
#### Success Response (CopyBothResponse)
Server responds with a `CopyBothResponse` message and then starts to stream WAL to the frontend. Includes two `CommandComplete` messages.

#### Error Response
Server can reply with an error, for example if the slot does not exist.
```

--------------------------------

### Create Table, View, and Grant Permissions

Source: https://www.postgresql.org/docs/current/rules-privileges.html

This example demonstrates creating a table, a view that filters data, and granting select privileges on the view to another user. Access to the underlying table is controlled by the owner of the view.

```sql
CREATE TABLE phone_data (person text, phone text, private boolean);
CREATE VIEW phone_number AS
    SELECT person, CASE WHEN NOT private THEN phone END AS phone
    FROM phone_data;
GRANT SELECT ON phone_number TO assistant;
```

--------------------------------

### Basic LATERAL Subquery Example in PostgreSQL

Source: https://www.postgresql.org/docs/current/queries-table-expressions.html

This example demonstrates a simple LATERAL subquery, allowing the subquery to reference columns from the 'foo' table.

```sql
SELECT * FROM foo, LATERAL (SELECT * FROM bar WHERE bar.id = foo.bar_id) ss;
```

--------------------------------

### Operator Precedence Example

Source: https://www.postgresql.org/docs/current/queries-union.html

This example demonstrates that INTERSECT has higher precedence than UNION or EXCEPT when multiple set operators are used without parentheses.

```SQL
_query1_ UNION _query2_ INTERSECT _query3_
```

--------------------------------

### Basic SQL LIKE Pattern Matching Examples

Source: https://www.postgresql.org/docs/current/functions-matching.html

Illustrates common LIKE operator usage with wildcards ('%' for any sequence, '_' for any single character) and literal string matching.

```SQL
'abc' LIKE 'abc'    _true_
'abc' LIKE 'a%'     _true_
'abc' LIKE '_b_'    _true_
'abc' LIKE 'c'      _false_
```

--------------------------------

### pg_ident.conf Regular Expression Mapping Example

Source: https://www.postgresql.org/docs/current/auth-username-maps.html

This example demonstrates how to use regular expressions in pg_ident.conf to map system usernames. It shows stripping domain parts and assigning a generic 'guest' role based on different domain patterns.

```plaintext
mymap   /^(.*)@mydomain\.com$      \1
mymap   /^(.*)@otherdomain\.com$   guest
```

--------------------------------

### Examples: Opening Bound Cursors with Positional and Named Arguments

Source: https://www.postgresql.org/docs/current/plpgsql-cursors.html

Illustrates various ways to open a bound cursor, including without arguments, with positional arguments, and with named arguments.

```plpgsql
OPEN curs2;
OPEN curs3(42);
OPEN curs3(key := 42);
OPEN curs3(key => 42);
```

--------------------------------

### SET DESCRIPTOR Examples — Embedded SQL

Source: https://www.postgresql.org/docs/current/ecpg-sql-set-descriptor.html

Embedded SQL examples showing SET DESCRIPTOR usage for setting descriptor header items and individual descriptor values. Demonstrates setting COUNT, DATA, and INDICATOR items with both SQL constants and host variables.

```sql
EXEC SQL SET DESCRIPTOR indesc COUNT = 1;
```

```sql
EXEC SQL SET DESCRIPTOR indesc VALUE 1 DATA = 2;
```

```sql
EXEC SQL SET DESCRIPTOR indesc VALUE 1 DATA = :val1;
```

```sql
EXEC SQL SET DESCRIPTOR indesc VALUE 2 INDICATOR = :val1, DATA = 'some string';
```

```sql
EXEC SQL SET DESCRIPTOR indesc VALUE 2 INDICATOR = :val2null, DATA = :val2;
```

--------------------------------

### Basic Syntax for SHOW Command in PostgreSQL

Source: https://www.postgresql.org/docs/current/sql-show.htm

Use `SHOW _name_` to display a specific run-time parameter or `SHOW ALL` to list all parameters and their current settings.

```sql
SHOW _name_
SHOW ALL
```

--------------------------------

### PostgreSQL NULLIF Example for Value Replacement

Source: https://www.postgresql.org/docs/current/functions-conditional.html

This example demonstrates how to use `NULLIF` to replace a specific string, '(none)', with NULL in a query result.

```sql
SELECT NULLIF(value, '(none)') ...
```

--------------------------------

### Create and Analyze a Multi-Column B-tree Index (PostgreSQL)

Source: https://www.postgresql.org/docs/current/bloom.html

This example creates a multi-column B-tree index on `tbloom` and then analyzes a query that still results in a sequential scan, demonstrating the B-tree's inefficiency when leading columns are not constrained.

```sql
=# CREATE INDEX btreeidx ON tbloom (i1, i2, i3, i4, i5, i6);
CREATE INDEX
=# SELECT pg_size_pretty(pg_relation_size('btreeidx'));
 pg_size_pretty
----------------
 386 MB
(1 row)
=# EXPLAIN ANALYZE SELECT * FROM tbloom WHERE i2 = 898732 AND i5 = 123451;
                                              QUERY PLAN
-------------------------------------------------------------------u200b-----------------------------------
 Seq Scan on tbloom  (cost=0.00..213744.00 rows=2 width=24) (actual time=351.016..351.017 rows=0.00 loops=1)
   Filter: ((i2 = 898732) AND (i5 = 123451))
   Rows Removed by Filter: 10000000
   Buffers: shared hit=63744
 Planning Time: 0.138 ms
 Execution Time: 351.035 ms
(6 rows)
```

--------------------------------

### Substring Function Examples with SIMILAR TO

Source: https://www.postgresql.org/docs/current/functions-matching.html

Illustrates how to use the `substring` function with `SIMILAR TO` patterns to extract parts of a string, including cases that return NULL.

```SQL
substring('foobar' similar '%#"o_b#"%' escape '#')   _oob_
substring('foobar' similar '#"o_b#"%' escape '#')    _NULL_
```

--------------------------------

### PostgreSQL to_char Function Examples

Source: https://www.postgresql.org/docs/current/functions-formatting.html

Examples demonstrating various formatting patterns and modifiers for the to_char function in PostgreSQL, including date/time, numeric, and special formats like Roman numerals. These snippets illustrate how different patterns affect the output string.

```SQL
to_char(current_timestamp, 'Day, DD  HH12:MI:SS')
```

```SQL
to_char(current_timestamp, 'FMDay, FMDD  HH12:MI:SS')
```

```SQL
to_char(current_timestamp AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS"Z"')
```

```SQL
to_char(-0.1, '99.99')
```

```SQL
to_char(-0.1, 'FM9.99')
```

```SQL
to_char(-0.1, 'FM90.99')
```

```SQL
to_char(0.1, '0.9')
```

```SQL
to_char(12, '9990999.9')
```

```SQL
to_char(12, 'FM9990999.9')
```

```SQL
to_char(485, '999')
```

```SQL
to_char(-485, '999')
```

```SQL
to_char(485, '9 9 9')
```

```SQL
to_char(1485, '9,999')
```

```SQL
to_char(1485, '9G999')
```

```SQL
to_char(148.5, '999.999')
```

```SQL
to_char(148.5, 'FM999.999')
```

```SQL
to_char(148.5, 'FM999.990')
```

```SQL
to_char(148.5, '999D999')
```

```SQL
to_char(3148.5, '9G999D999')
```

```SQL
to_char(-485, '999S')
```

```SQL
to_char(-485, '999MI')
```

```SQL
to_char(485, '999MI')
```

```SQL
to_char(485, 'FM999MI')
```

```SQL
to_char(485, 'PL999')
```

```SQL
to_char(485, 'SG999')
```

```SQL
to_char(-485, 'SG999')
```

```SQL
to_char(-485, '9SG99')
```

```SQL
to_char(-485, '999PR')
```

```SQL
to_char(485, 'L999')
```

```SQL
to_char(485, 'RN')
```

```SQL
to_char(485, 'FMRN')
```

```SQL
to_char(5.2, 'FMRN')
```

```SQL
to_char(482, '999th')
```

```SQL
to_char(485, '"Good number:"999')
```

```SQL
to_char(485.8, '"Pre:"999" Post:" .999')
```

```SQL
to_char(12, '99V999')
```

```SQL
to_char(12.4, '99V999')
```

```SQL
to_char(12.45, '99V9')
```

```SQL
to_char(0.0004859, '9.99EEEE')
```

--------------------------------

### Example: Receiving Notifications with dblink_get_notify

Source: https://www.postgresql.org/docs/current/contrib-dblink-get-notify.html

Demonstrates how to use dblink_exec to LISTEN for notifications, then retrieve them using dblink_get_notify after a NOTIFY command.

```sql
SELECT dblink_exec('LISTEN virtual');
 dblink_exec
-------------
 LISTEN
(1 row)

SELECT * FROM dblink_get_notify();
 notify_name | be_pid | extra
-------------+--------+-------
(0 rows)

NOTIFY virtual;
NOTIFY

SELECT * FROM dblink_get_notify();
 notify_name | be_pid | extra
-------------
 virtual     |   1229 |
(1 row)
```

--------------------------------

### Initialize Shared Memory with LWLock Protection (C)

Source: https://www.postgresql.org/docs/current/xfunc-c.html

This example demonstrates how to safely initialize shared memory using `ShmemInitStruct` by acquiring `AddinShmemInitLock` to prevent race conditions among backends.

```C
static mystruct *ptr = NULL;
bool        found;

LWLockAcquire(AddinShmemInitLock, LW_EXCLUSIVE);
ptr = ShmemInitStruct("my struct name", size, &found);
if (!found)
{
    ... initialize contents of shared memory ...
    ptr->locks = GetNamedLWLockTranche("my tranche name");
}
LWLockRelease(AddinShmemInitLock);
```

--------------------------------

### Analyze URL tokenization with ts_debug

Source: https://www.postgresql.org/docs/current/textsearch-parsers.html

This example shows how the default parser identifies protocol, host, and path components within a URL string.

```sql
SELECT alias, description, token FROM ts_debug('http://example.com/stuff/index.html');
  alias   |  description  |            token
----------+---------------+------------------------------
 protocol | Protocol head | http://
 url      | URL           | example.com/stuff/index.html
 host     | Host          | example.com
 url_path | URL path      | /stuff/index.html

```

--------------------------------

### Query View Before Updates

Source: https://www.postgresql.org/docs/current/rules-update.html

Example query showing the current state of the shoelace view before applying updates through rules.

```SQL
SELECT * FROM shoelace;

 sl_name  | sl_avail | sl_color | sl_len | sl_unit | sl_len_cm
----------+----------+----------+--------+---------+-----------
 sl1      |        5 | black    |     80 | cm      |        80
 sl2      |        6 | black    |    100 | cm      |       100
 sl7      |        6 | brown    |     60 | cm      |        60
 sl3      |        0 | black    |     35 | inch    |      88.9
 sl4      |        8 | black    |     40 | inch    |     101.6
 sl8      |        1 | brown    |     40 | inch    |     101.6
 sl5      |        4 | brown    |      1 | m       |       100
 sl6      |        0 | brown    |    0.9 | m       |        90
(8 rows)
```

--------------------------------

### SELECT * FROM pg_available_extension_versions

Source: https://www.postgresql.org/docs/current/view-pg-available-extension-versions.html

The pg_available_extension_versions view lists the specific extension versions that are available for installation on the PostgreSQL server.

```APIDOC
## SELECT pg_available_extension_versions

### Description
The pg_available_extension_versions view lists the specific extension versions that are available for installation. It is a read-only system view.

### Method
SELECT

### Endpoint
pg_available_extension_versions

### Response
#### Success Response (200)
- **name** (name) - Extension name
- **version** (text) - Version name
- **installed** (bool) - True if this version of this extension is currently installed
- **superuser** (bool) - True if only superusers are allowed to install this extension (but see trusted)
- **trusted** (bool) - True if the extension can be installed by non-superusers with appropriate privileges
- **relocatable** (bool) - True if extension can be relocated to another schema
- **schema** (name) - Name of the schema that the extension must be installed into, or NULL if partially or fully relocatable
- **requires** (name[]) - Names of prerequisite extensions, or NULL if none
- **comment** (text) - Comment string from the extension's control file

### Response Example
{
  "name": "plpgsql",
  "version": "1.0",
  "installed": true,
  "superuser": false,
  "trusted": true,
  "relocatable": false,
  "schema": "pg_catalog",
  "requires": null,
  "comment": "PL/pgSQL procedural language"
}
```

--------------------------------

### START TRANSACTION Syntax

Source: https://www.postgresql.org/docs/current/sql-start-transaction.html

Defines the syntax for starting a transaction block, including optional transaction modes like isolation level and access mode.

```sql
START TRANSACTION [ _transaction_mode_ [, ...] ]

where _transaction_mode_ is one of:

    ISOLATION LEVEL { SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED }
    READ WRITE | READ ONLY
    [ NOT ] DEFERRABLE
```

--------------------------------

### Prepare a statement with placeholders for input parameters

Source: https://www.postgresql.org/docs/current/ecpg-descriptors.html

Declare a query string with '?' placeholders for parameters and prepare it using `EXEC SQL PREPARE`.

```C
EXEC SQL BEGIN DECLARE SECTION;
char query[1024] = "SELECT d.oid, * FROM pg_database d, pg_stat_database s WHERE d.oid = s.datid AND (d.datname = ? OR d.oid = ?)";
EXEC SQL END DECLARE SECTION;

EXEC SQL PREPARE stmt1 FROM :query;
```

--------------------------------

### Dynamic SQL Execution with SQLDA in ECPG

Source: https://www.postgresql.org/docs/current/ecpg-descriptors.html

Demonstrates preparing a statement, setting up an input descriptor, and fetching results into an output descriptor using sqlda_t.

```c
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    EXEC SQL PREPARE stmt1 FROM :query;
    EXEC SQL DECLARE cur1 CURSOR FOR stmt1;

    /* Create an SQLDA structure for an input parameter */
    sqlda2 = (sqlda_t *)malloc(sizeof(sqlda_t) + sizeof(sqlvar_t));
    memset(sqlda2, 0, sizeof(sqlda_t) + sizeof(sqlvar_t));
    sqlda2->sqln = 2; /* a number of input variables */

    sqlda2->sqlvar[0].sqltype = ECPGt_char;
    sqlda2->sqlvar[0].sqldata = "postgres";
    sqlda2->sqlvar[0].sqllen  = 8;

    intval = 1;
    sqlda2->sqlvar[1].sqltype = ECPGt_int;
    sqlda2->sqlvar[1].sqldata = (char *) &intval;
    sqlda2->sqlvar[1].sqllen  = sizeof(intval);

    /* Open a cursor with input parameters. */
    EXEC SQL OPEN cur1 USING DESCRIPTOR sqlda2;

    while (1)
    {
        sqlda_t *cur_sqlda;

        /* Assign descriptor to the cursor  */
        EXEC SQL FETCH NEXT FROM cur1 INTO DESCRIPTOR sqlda1;

        for (cur_sqlda = sqlda1 ;
             cur_sqlda != NULL ;
             cur_sqlda = cur_sqlda->desc_next)
        {
            int i;
            char name_buf[1024];
            char var_buf[1024];

            /* Print every column in a row. */
            for (i=0 ; i<cur_sqlda->sqld ; i++)
            {
                sqlvar_t v = cur_sqlda->sqlvar[i];
                char *sqldata = v.sqldata;
                short sqllen  = v.sqllen;

                strncpy(name_buf, v.sqlname.data, v.sqlname.length);
                name_buf[v.sqlname.length] = '\0';

                switch (v.sqltype)
                {
                    case ECPGt_char:
                        memset(&var_buf, 0, sizeof(var_buf));
                        memcpy(&var_buf, sqldata, (sizeof(var_buf)<=sqllen ? sizeof(var_buf)-1 : sqllen) );
                        break;

                    case ECPGt_int: /* integer */
                        memcpy(&intval, sqldata, sqllen);
                        snprintf(var_buf, sizeof(var_buf), "%d", intval);
                        break;

                    case ECPGt_long_long: /* bigint */
                        memcpy(&longlongval, sqldata, sqllen);
                        snprintf(var_buf, sizeof(var_buf), "%lld", longlongval);
                        break;

                    default:
                    {
                        int i;
                        memset(var_buf, 0, sizeof(var_buf));
                        for (i = 0; i < sqllen; i++)
                        {
                            char tmpbuf[16];
                            snprintf(tmpbuf, sizeof(tmpbuf), "%02x ", (unsigned char) sqldata[i]);
                            strncat(var_buf, tmpbuf, sizeof(var_buf));
                        }
                    }
                        break;
                }

                printf("%s = %s (type: %d)\n", name_buf, var_buf, v.sqltype);
            }

            printf("\n");
        }
    }

    EXEC SQL CLOSE cur1;
    EXEC SQL COMMIT;

    EXEC SQL DISCONNECT ALL;

    return 0;
}
```

--------------------------------

### Configure MANPATH for PostgreSQL documentation

Source: https://www.postgresql.org/docs/current/install-post.html

Add the PostgreSQL man documentation directory to the MANPATH environment variable. Add this to your shell start-up file unless PostgreSQL was installed in a default system location.

```bash
MANPATH=/usr/local/pgsql/share/man:$MANPATH
export MANPATH
```

--------------------------------

### Start PostgreSQL server as the postgres user

Source: https://www.postgresql.org/docs/current/server-start.html

Ensure the server is never run as root; use su to execute the startup command as the dedicated PostgreSQL user account.

```shell
su postgres -c 'pg_ctl start -D /usr/local/pgsql/data -l serverlog'

```

--------------------------------

### Create logical replication subscriptions in PostgreSQL

Source: https://www.postgresql.org/docs/current/sql-createsubscription.html

Examples of creating subscriptions to remote servers with immediate replication or in a disabled state.

```sql
CREATE SUBSCRIPTION mysub
         CONNECTION 'host=192.168.1.50 port=5432 user=foo dbname=foodb'
        PUBLICATION mypublication, insert_only;

```

```sql
CREATE SUBSCRIPTION mysub
         CONNECTION 'host=192.168.1.50 port=5432 user=foo dbname=foodb'
        PUBLICATION insert_only
               WITH (enabled = false);

```

--------------------------------

### CREATE DATABASE Syntax

Source: https://www.postgresql.org/docs/current/sql-createdatabase.htm

Complete syntax for the CREATE DATABASE command with all available parameters for configuring a new database.

```sql
CREATE DATABASE _name_
    [ WITH ] [ OWNER [=] _user_name_ ]
           [ TEMPLATE [=] _template_ ]
           [ ENCODING [=] _encoding_ ]
           [ STRATEGY [=] _strategy_ ]
           [ LOCALE [=] _locale_ ]
           [ LC_COLLATE [=] _lc_collate_ ]
           [ LC_CTYPE [=] _lc_ctype_ ]
           [ BUILTIN_LOCALE [=] _builtin_locale_ ]
           [ ICU_LOCALE [=] _icu_locale_ ]
           [ ICU_RULES [=] _icu_rules_ ]
           [ LOCALE_PROVIDER [=] _locale_provider_ ]
           [ COLLATION_VERSION = _collation_version_ ]
           [ TABLESPACE [=] _tablespace_name_ ]
           [ ALLOW_CONNECTIONS [=] _allowconn_ ]
           [ CONNECTION LIMIT [=] _connlimit_ ]
           [ IS_TEMPLATE [=] _istemplate_ ]
           [ OID [=] _oid_ ]
```

--------------------------------

### Typical pg_stat_statements configuration

Source: https://www.postgresql.org/docs/current/pgstatstatements.html

Example configuration for postgresql.conf to enable statement tracking. Requires shared_preload_libraries to include the module.

```ini
# postgresql.conf
shared_preload_libraries = 'pg_stat_statements'

compute_query_id = on
pg_stat_statements.max = 10000
pg_stat_statements.track = all

```

--------------------------------

### Create a database using an absolute path

Source: https://www.postgresql.org/docs/current/tutorial-createdb.html

Use the full path to the utility if it is not in your shell's search path.

```shell
$ **/usr/local/pgsql/bin/createdb mydb**
```

--------------------------------

### Example: Retrieve Last Error Message

Source: https://www.postgresql.org/docs/current/contrib-dblink-error-message.html

This example demonstrates how to use `dblink_error_message` to fetch the last error message from a dblink connection named 'dtest1'.

```SQL
SELECT dblink_error_message('dtest1');
```

--------------------------------

### SQLDA Basic Usage

Source: https://www.postgresql.org/docs/current/ecpg-descriptors.html

Demonstrates basic SQLDA usage including including the sqlda.h header, declaring an SQLDA pointer, and fetching rows into a descriptor. Shows how the DESCRIPTOR keyword can be omitted when using the INTO keyword with DESCRIBE statements.

```APIDOC
## SQLDA Basic Usage

### Description
Basic usage pattern for SQLDA descriptor areas in PostgreSQL ECPG, including header inclusion, variable declaration, and fetching data into descriptors.

### Include Header
```c
EXEC SQL include sqlda.h;
```

### Declare SQLDA Pointer
```c
sqlda_t *mysqlda;
```

### Fetch Rows into Descriptor
```c
EXEC SQL FETCH 3 FROM mycursor INTO DESCRIPTOR mysqlda;
```

### Describe Statement (DESCRIPTOR keyword optional with INTO)
```c
EXEC SQL DESCRIBE prepared_statement INTO mysqlda;
```

### Notes
- The SQL keyword is omitted in SQLDA operations
- The DESCRIPTOR keyword can be omitted if the INTO keyword is used in DESCRIBE statements
- INTO and USING keywords follow the same use cases as described in Section 34.7.1
```

--------------------------------

### Verify backup with external manifest file

Source: https://www.postgresql.org/docs/current/app-pgverifybackup.html

Create a backup, move the manifest file to a secure location outside the backup directory, then verify the backup using the external manifest path.

```bash
$ pg_basebackup -h mydbserver -D /usr/local/pgsql/backup1234
$ mv /usr/local/pgsql/backup1234/backup_manifest /my/secure/location/backup_manifest.1234
$ pg_verifybackup -m /my/secure/location/backup_manifest.1234 /usr/local/pgsql/backup1234
```

--------------------------------

### Example PostgreSQL Injection Point Callback Function

Source: https://www.postgresql.org/docs/current/xfunc-c.html

This is an example of a callback function that can be attached to an injection point. It prints a notice message to the server error log.

```C
static void
custom_injection_callback(const char *name,
                          const void *private_data,
                          void *arg)
{
    uint32 wait_event_info = WaitEventInjectionPointNew(name);

    pgstat_report_wait_start(wait_event_info);
    elog(NOTICE, "%s: executed custom callback", name);
    pgstat_report_wait_end();
}
```

--------------------------------

### Perform documentation syntax check using Make

Source: https://www.postgresql.org/docs/current/docguide-build.html

A fast method to verify the SGML syntax of documentation files without performing a full build.

```shell
doc/src/sgml$ **make check**

```

--------------------------------

### Add Tables and Schemas to a Publication

Source: https://www.postgresql.org/docs/current/sql-alterpublication.html

This example combines adding specific tables and all tables within a schema to an existing publication in a single command.

```SQL
ALTER PUBLICATION production_publication ADD TABLE users, departments, TABLES IN SCHEMA production;

```

--------------------------------

### Build PostgreSQL with Documentation and Contrib Modules

Source: https://www.postgresql.org/docs/current/install-make.html

This command builds everything possible, including HTML and man page documentation, and additional `contrib` modules. It's a comprehensive build option.

```make
make world
```

--------------------------------

### PL/Perl Event Trigger Function Example

Source: https://www.postgresql.org/docs/current/plperl-event-triggers.html

This example demonstrates how to create a PL/Perl event trigger function that logs event details and then associates it with the ddl_command_start event.

```SQL
CREATE OR REPLACE FUNCTION perlsnitch() RETURNS event_trigger AS $$
  elog(NOTICE, "perlsnitch: " . $_TD->{event} . " " . $_TD->{tag} . " ");
$$ LANGUAGE plperl;

CREATE EVENT TRIGGER perl_a_snitch
    ON ddl_command_start
    EXECUTE FUNCTION perlsnitch();
```

--------------------------------

### Create Table and Analyze for Multivariate Statistics Example

Source: https://www.postgresql.org/docs/current/multivariate-statistics-examples.html

This snippet creates a sample table 't' with two integer columns, 'a' and 'b', populates it with 10,000 rows where 'a' and 'b' contain identical values, and then runs 'ANALYZE' to collect initial statistics.

```SQL
CREATE TABLE t (a INT, b INT);
INSERT INTO t SELECT i % 100, i % 100 FROM generate_series(1, 10000) s(i);
ANALYZE t;
```

--------------------------------

### Example of closing a remote cursor

Source: https://www.postgresql.org/docs/current/contrib-dblink-close.html

Demonstrates the full lifecycle of connecting to a remote database, opening a cursor, and closing it.

```sql
SELECT dblink_connect('dbname=postgres options=-csearch_path=');
 dblink_connect
----------------
 OK
(1 row)

SELECT dblink_open('foo', 'select proname, prosrc from pg_proc');
 dblink_open
-------------
 OK
(1 row)

SELECT dblink_close('foo');
 dblink_close
--------------
 OK
(1 row)
```

--------------------------------

### xmlelement: Invalid attribute name examples

Source: https://www.postgresql.org/docs/current/functions-xml.html

These examples show invalid uses: constants and function results in XMLATTRIBUTES require explicit names, and cannot be used without them.

```sql
SELECT xmlelement(name test, xmlattributes('constant'), a, b) FROM test;
SELECT xmlelement(name test, xmlattributes(func(a, b))) FROM test;
```

--------------------------------

### PostgreSQL Connection URI Examples

Source: https://www.postgresql.org/docs/current/libpq-connect.html

Various valid URI formats for local, remote, authenticated, and multi-host connections.

```plaintext
postgresql://
postgresql://localhost
postgresql://localhost:5433
postgresql://localhost/mydb
postgresql://user@localhost
postgresql://user:secret@localhost
postgresql://other@localhost/otherdb?connect_timeout=10&application_name=myapp
postgresql://host1:123,host2:456/somedb?target_session_attrs=any&application_name=myapp
```

--------------------------------

### Set search_path for extension installation

Source: https://www.postgresql.org/docs/current/extend-extensions.html

The search_path is automatically configured during CREATE EXTENSION to point to the target schema and pg_temp.

```sql
SET LOCAL search_path TO @extschema@, pg_temp;

```

--------------------------------

### OPEN Command Syntax

Source: https://www.postgresql.org/docs/current/ecpg-sql-open.html

Outlines the various syntaxes for the `OPEN` command, including options for simple cursor opening, binding multiple values, and using a SQL descriptor.

```SQL
OPEN _cursor_name_
OPEN _cursor_name_ USING _value_ [, ... ]
OPEN _cursor_name_ USING SQL DESCRIPTOR _descriptor_name_
```

--------------------------------

### SELECT * FROM pg_available_extensions

Source: https://www.postgresql.org/docs/current/view-pg-available-extensions.html

The pg_available_extensions view lists the extensions that are available for installation on the PostgreSQL server. It provides details on the extension name, default version, and currently installed version.

```APIDOC
## SELECT * FROM pg_available_extensions

### Description
The pg_available_extensions view lists the extensions that are available for installation. See also the pg_extension catalog, which shows the extensions currently installed.

### Method
SELECT

### Endpoint
pg_available_extensions

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
SELECT * FROM pg_available_extensions;

### Response
#### Success Response (200)
- **name** (name) - Extension name
- **default_version** (text) - Name of default version, or NULL if none is specified
- **installed_version** (text) - Currently installed version of the extension, or NULL if not installed
- **comment** (text) - Comment string from the extension's control file

#### Response Example
[
  {
    "name": "plpgsql",
    "default_version": "1.0",
    "installed_version": "1.0",
    "comment": "PL/pgSQL procedural language"
  }
]
```

--------------------------------

### CREATE USER Syntax Synopsis

Source: https://www.postgresql.org/docs/current/sql-createuser.htm

Full syntax for the CREATE USER command including all available role options and attributes.

```sql
CREATE USER _name_ [ [ WITH ] _option_ [ ... ] ]

where _option_ can be:

      SUPERUSER | NOSUPERUSER
    | CREATEDB | NOCREATEDB
    | CREATEROLE | NOCREATEROLE
    | INHERIT | NOINHERIT
    | LOGIN | NOLOGIN
    | REPLICATION | NOREPLICATION
    | BYPASSRLS | NOBYPASSRLS
    | CONNECTION LIMIT _connlimit_
    | [ ENCRYPTED ] PASSWORD '_password_' | PASSWORD NULL
    | VALID UNTIL '_timestamp_'
    | IN ROLE _role_name_ [, ...]
    | IN GROUP _role_name_ [, ...]
    | ROLE _role_name_ [, ...]
    | ADMIN _role_name_ [, ...]
    | USER _role_name_ [, ...]
    | SYSID _uid_
```

--------------------------------

### FUNCTION substr

Source: https://www.postgresql.org/docs/current/functions-binarystring.html

Extracts a substring from a binary string, starting at a specified byte index and optionally for a given length. This function is equivalent to substring(bytes from start for count).

```APIDOC
## FUNCTION substr

### Description
Extracts the substring of bytes starting at the start'th byte, and extending for count bytes if that is specified.

### Method
Function Call

### Endpoint
substr(bytes bytea, start integer [, count integer ])

### Parameters
#### Function Parameters
- **bytes** (bytea) - The source binary string.
- **start** (integer) - The starting byte index (1-indexed).
- **count** (integer) - Optional. The number of bytes to extract.

### Request Example
```sql
SELECT substr('\x1234567890'::bytea, 3, 2);
```

### Response
#### Return Type (bytea)
- Returns the extracted substring as a bytea.

#### Response Example
```
\x5678
```
```

--------------------------------

### SET ROLE Example with User Context

Source: https://www.postgresql.org/docs/current/sql-set-role.html

Demonstrates switching roles within a session and observing the change in SESSION_USER and CURRENT_USER. SESSION_USER remains the authenticated user (peter), while CURRENT_USER reflects the active role (paul).

```sql
SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user
--------------+--------------
 peter        | peter

SET ROLE 'paul';

SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user
--------------+--------------
 peter        | paul
```

--------------------------------

### Define PostgreSQL Module Name and Version (C)

Source: https://www.postgresql.org/docs/current/xfunc-c.html

Example of using 'PG_MODULE_MAGIC_EXT' to set the module's name and version string for identification.

```C
PG_MODULE_MAGIC_EXT(
    .name = "my_module_name",
    .version = "1.2.3"
);
```

--------------------------------

### Basic SQL Command Examples

Source: https://www.postgresql.org/docs/current/sql-syntax-lexical.html

This snippet demonstrates a sequence of three common SQL commands: SELECT, UPDATE, and INSERT, illustrating how commands are structured and terminated.

```SQL
SELECT * FROM MY_TABLE;
UPDATE MY_TABLE SET A = 5;
INSERT INTO MY_TABLE VALUES (3, 'hi there');

```

--------------------------------

### Merge Join Plan Example

Source: https://www.postgresql.org/docs/current/using-explain.html

Illustrates a merge join which requires both input relations to be sorted on the join keys.

```sql
EXPLAIN SELECT *
FROM tenk1 t1, onek t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2;

                                        QUERY PLAN
-------------------------------------------------------------------​-----------------------
 Merge Join  (cost=0.56..233.49 rows=10 width=488)
   Merge Cond: (t1.unique2 = t2.unique2)
   ->  Index Scan using tenk1_unique2 on tenk1 t1  (cost=0.29..643.28 rows=100 width=244)
         Filter: (unique1 < 100)
   ->  Index Scan using onek_unique2 on onek t2  (cost=0.28..166.28 rows=1000 width=244)
```

--------------------------------

### Frontend Implementation Recommendations

Source: https://www.postgresql.org/docs/current/protocol-flow.html

Best practices for implementing PostgreSQL frontend clients to properly handle the simple query protocol.

```APIDOC
## Frontend Implementation Recommendations

### State-Machine Style
Recommended practice is to code frontends in a state-machine style that will accept any message type at any time that it could make sense, rather than wiring in assumptions about the exact sequence of messages.

### Message Handling
- Frontend must be prepared to accept ErrorResponse and NoticeResponse messages whenever it is expecting any other type of message
- Frontend should display NoticeResponse messages but continue listening for ReadyForQuery or ErrorResponse
- Frontend should handle all possible response message types

### Command Sequencing
- Frontend does not need to wait for ReadyForQuery before sending another Query message
- However, if the frontend does not wait, it must take responsibility for figuring out what happens if an earlier command fails and already-issued later commands succeed
- Recommended practice is to wait for ReadyForQuery before sending the next command

### Message Types to Handle
- CommandComplete
- CopyInResponse
- CopyOutResponse
- RowDescription
- DataRow
- EmptyQueryResponse
- ErrorResponse
- ReadyForQuery
- NoticeResponse
```

--------------------------------

### COMMIT PREPARED - Example with Transaction ID

Source: https://www.postgresql.org/docs/current/sql-commit-prepared.html

Commits a specific prepared transaction identified by 'foobar'. This example demonstrates the typical usage pattern for committing a prepared transaction.

```SQL
COMMIT PREPARED 'foobar';
```

--------------------------------

### PostgreSQL postgres_fdw Module Overview

Source: https://www.postgresql.org/docs/current/postgres-fdw.html

Comprehensive guide to setting up and using the `postgres_fdw` module for accessing external PostgreSQL servers.

```APIDOC
## postgres_fdw Module

### Description
The `postgres_fdw` module provides a foreign-data wrapper to access data stored in external PostgreSQL servers. It offers a more transparent and standards-compliant syntax compared to the older dblink module, often with better performance.

### Operations
This module enables several database operations for remote data access and manipulation.

### Setup Steps
1. **Install Extension**: Use `CREATE EXTENSION postgres_fdw;`
2. **Create Foreign Server**: Use `CREATE SERVER` to define connection details for the remote database.
3. **Create User Mapping**: Use `CREATE USER MAPPING` to specify remote user credentials.
4. **Create Foreign Table**: Use `CREATE FOREIGN TABLE` or `IMPORT FOREIGN SCHEMA` to map remote tables locally.

### Data Access and Manipulation
Once set up, remote tables can be accessed and modified using standard SQL commands:
- `SELECT`: Retrieve data from foreign tables.
- `INSERT`: Add new rows to foreign tables.
- `UPDATE`: Modify existing rows in foreign tables.
- `DELETE`: Remove rows from foreign tables.
- `COPY`: Copy data to or from foreign tables.
- `TRUNCATE`: Empty foreign tables.

### Limitations and Recommendations
- The `ONLY` option in `SELECT`, `UPDATE`, `DELETE`, or `TRUNCATE` has no effect on remote tables.
- `INSERT ... ON CONFLICT DO UPDATE` is not supported, but `ON CONFLICT DO NOTHING` is (without unique index inference).
- Row movement by `UPDATE` on partitioned tables is supported, but not when the remote partition for insertion is also an `UPDATE` target.
- **Recommendation**: Declare foreign table columns with exactly the same data types and collations as the remote table to avoid semantic anomalies.
- Foreign tables can have fewer columns or a different order; matching is by name.
```

--------------------------------

### DROP SERVER - Drop Existing Server Example

Source: https://www.postgresql.org/docs/current/sql-dropserver.html

Drops a server named 'foo' only if it exists, suppressing errors if the server is not found.

```sql
DROP SERVER IF EXISTS foo;
```

--------------------------------

### Change User Mapping Password Example

Source: https://www.postgresql.org/docs/current/sql-alterusermapping.html

This example demonstrates how to use ALTER USER MAPPING to change the 'password' option for a specific user mapping on a foreign server.

```sql
ALTER USER MAPPING FOR bob SERVER foo OPTIONS (SET password 'public');
```

--------------------------------

### Examine Query Plan for Prepared Statement (PostgreSQL)

Source: https://www.postgresql.org/docs/current/sql-prepare.html

Use EXPLAIN to view the query plan for a prepared statement. The plan will show parameter symbols for generic plans or substituted values for custom plans.

```sql
EXPLAIN EXECUTE _name_(_parameter_values_);
```

--------------------------------

### ALTER OPERATOR FAMILY - DROP Example

Source: https://www.postgresql.org/docs/current/sql-alteropfamily.html

Practical example demonstrating how to remove operators and support functions from an operator family by specifying strategy numbers and data types.

```APIDOC
## ALTER OPERATOR FAMILY - DROP

### Description
Removes operators and support functions from an operator family. The DROP syntax specifies the "slot" in the operator family by strategy or support number and input data type(s), without needing to specify the actual operator or function name.

### Example
To remove the entries added in the previous example:

```sql
ALTER OPERATOR FAMILY integer_ops USING btree DROP

  -- int4 vs int2
  OPERATOR 1 (int4, int2) ,
  OPERATOR 2 (int4, int2) ,
  OPERATOR 3 (int4, int2) ,
  OPERATOR 4 (int4, int2) ,
  OPERATOR 5 (int4, int2) ,
  FUNCTION 1 (int4, int2) ,

  -- int2 vs int4
  OPERATOR 1 (int2, int4) ,
  OPERATOR 2 (int2, int4) ,
  OPERATOR 3 (int2, int4) ,
  OPERATOR 4 (int2, int4) ,
  OPERATOR 5 (int2, int4) ,
  FUNCTION 1 (int2, int4) ;
```

### Explanation
- **OPERATOR clauses**: Specify the strategy number and operand data types to remove
- **FUNCTION clauses**: Specify the support function number and operand data types to remove
- The actual operator and function names are not required in the DROP syntax
- Only the "slot" (strategy/support number and data types) needs to be specified
```

--------------------------------

### Explain Query Plan with YAML Output in PostgreSQL

Source: https://www.postgresql.org/docs/current/sql-explain.htm

Format the EXPLAIN output as YAML for an alternative structured representation.

```sql
EXPLAIN (FORMAT YAML) SELECT * FROM foo WHERE i='4';
          QUERY PLAN
-------------------------------
 - Plan:
     Node Type: "Index Scan"
     Scan Direction: "Forward"
     Index Name: "fi"
     Relation Name: "foo"
     Alias: "foo"
     Startup Cost: 0.00
     Total Cost: 5.98
     Plan Rows: 1
     Plan Width: 4
     Index Cond: "(i = 4)"
(1 row)
```

--------------------------------

### SIMILAR TO Operator Examples

Source: https://www.postgresql.org/docs/current/functions-matching.html

Demonstrates various uses of the `SIMILAR TO` operator with different patterns and strings, illustrating true/false outcomes.

```SQL
'abc' SIMILAR TO 'abc'          _true_
'abc' SIMILAR TO 'a'            _false_
'abc' SIMILAR TO '%(b|d)%'      _true_
'abc' SIMILAR TO '(b|c)%'       _false_
'-abc-' SIMILAR TO '%\mabc\M%'  _true_
'xabcy' SIMILAR TO '%\mabc\M%'  _false_
```

--------------------------------

### Configure PostgreSQL for Custom Extension Paths

Source: https://www.postgresql.org/docs/current/extend-pgxs.html

Add these lines to 'postgresql.conf' to enable the server to locate extension files and shared libraries installed in custom directories.

```configuration
extension_control_path = '/usr/local/extras/share/postgresql:$system'
dynamic_library_path = '/usr/local/extras/lib/postgresql:$libdir'
```

--------------------------------

### Install bool_plperl extension for boolean transforms

Source: https://www.postgresql.org/docs/current/plperl-funcs.html

Install the bool_plperl extension to enable proper boolean value handling in PL/Perl, converting PostgreSQL bool to Perl true/false values.

```sql
CREATE EXTENSION bool_plperl;  -- or bool_plperlu for PL/PerlU
```

--------------------------------

### Initialize SSL Library with PQinitSSL (C)

Source: https://www.postgresql.org/docs/current/libpq-ssl.html

This function allows applications to indicate that SSL libraries have been initialized. It is equivalent to `PQinitOpenSSL(do_ssl, do_ssl)` and is deprecated.

```C
void PQinitSSL(int do_ssl);
```

--------------------------------

### Control PostgreSQL Server Lifecycle

Source: https://www.postgresql.org/docs/current/logical-replication-upgrade.html

Use pg_ctl to stop the old instance or start the upgraded instance on either node.

```shell
pg_ctl -D /opt/PostgreSQL/data1 stop

```

```shell
pg_ctl -D /opt/PostgreSQL/data1_upgraded start -l logfile

```

```shell
pg_ctl -D /opt/PostgreSQL/data2 stop

```

```shell
pg_ctl -D /opt/PostgreSQL/data2_upgraded start -l logfile

```

--------------------------------

### Create Database with Remote Host, Port, and Template

Source: https://www.postgresql.org/docs/current/app-createdb.htm

Creates a database on a specified remote host and port, using a custom template. The `-e` flag shows the equivalent SQL command.

```bash
$ **createdb -p 5000 -h eden -T template0 -e demo**
```

```sql
CREATE DATABASE demo TEMPLATE template0;
```

--------------------------------

### Start psql and enter SQL commands

Source: https://www.postgresql.org/docs/current/app-psql.htm

Launch psql connected to a database and interact with the prompt. Commands are sent to the server when a semicolon is reached; line breaks do not terminate commands.

```bash
$ psql testdb
psql (18.3)
Type "help" for help.

testdb=>
```

--------------------------------

### Build man pages using Make

Source: https://www.postgresql.org/docs/current/docguide-build.html

Uses DocBook XSL stylesheets to convert refentry pages into roff format.

```shell
doc/src/sgml$ **make man**

```

--------------------------------

### CopyBothResponse (B) - Start Copy Both

Source: https://www.postgresql.org/docs/current/protocol-message-formats.html

Sent by the backend to indicate the start of a COPY BOTH operation, used only for Streaming Replication. Specifies the overall copy format and format codes for each column.

```APIDOC
## CopyBothResponse (B)

### Description
Identifies the message as a Start Copy Both response. This message is used only for Streaming Replication.

### Message Format

| Field | Type | Description |
|-------|------|-------------|
| Message Type | Byte1 | 'W' - Identifies the message as a Start Copy Both response |
| Length | Int32 | Length of message contents in bytes, including self |
| Format | Int8 | 0 = textual format (rows separated by newlines, columns by separator); 1 = binary format (similar to DataRow format) |
| Column Count | Int16 | The number of columns in the data to be copied (N) |
| Format Codes | Int16[N] | The format codes for each column. Each must be 0 (text) or 1 (binary). All must be 0 if overall copy format is textual |

### Notes
- Used exclusively for Streaming Replication
- Format code 0 indicates text format
- Format code 1 indicates binary format
- All format codes must be 0 if the overall copy format is textual
```

--------------------------------

### Hash Join Plan Example

Source: https://www.postgresql.org/docs/current/using-explain.html

Shows a hash join strategy where one table is hashed in memory to facilitate fast probing from the other table.

```sql
EXPLAIN SELECT *
FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 100 AND t1.unique2 = t2.unique2;

                                        QUERY PLAN
-------------------------------------------------------------------​-----------------------
 Hash Join  (cost=226.23..709.73 rows=100 width=488)
   Hash Cond: (t2.unique2 = t1.unique2)
   ->  Seq Scan on tenk2 t2  (cost=0.00..445.00 rows=10000 width=244)
   ->  Hash  (cost=224.98..224.98 rows=100 width=244)
         ->  Bitmap Heap Scan on tenk1 t1  (cost=5.06..224.98 rows=100 width=244)
               Recheck Cond: (unique1 < 100)
               ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
                     Index Cond: (unique1 < 100)
```

--------------------------------

### GET DESCRIPTOR - Header Form

Source: https://www.postgresql.org/docs/current/ecpg-sql-get-descriptor.html

Retrieves descriptor header items that apply to the entire result set. Currently supports COUNT to get the number of columns in the result set.

```APIDOC
## GET DESCRIPTOR (Header Form)

### Description
Retrieves descriptor header items that apply to the entire result set from an SQL descriptor area and stores the information into a host variable.

### Syntax
```
GET DESCRIPTOR descriptor_name :cvariable = descriptor_header_item [, ... ]
```

### Parameters
- **descriptor_name** (string) - Required - The name of the descriptor area to retrieve information from
- **descriptor_header_item** (token) - Required - Header information item to retrieve. Currently supported: COUNT (number of columns in result set)
- **cvariable** (host variable) - Required - Host variable that will receive the retrieved data

### Request Example
```
EXEC SQL GET DESCRIPTOR d :d_count = COUNT;
```

### Response
The specified host variable receives the requested header information value.

### Response Example
```
d_count = 1
```
```

--------------------------------

### Create logical replica with pg_createsubscriber

Source: https://www.postgresql.org/docs/current/app-pgcreatesubscriber.html

Command to convert physical replicas of databases 'hr' and 'finance' from source server 'foo' into logical replicas. Specify the target data directory with -D, source connection string with -P, and databases with -d flags.

```bash
$ pg_createsubscriber -D /usr/local/pgsql/data -P "host=foo" -d hr -d finance
```

--------------------------------

### Savepoint Lock Preservation Example

Source: https://www.postgresql.org/docs/current/sql-select.htm

Example demonstrating lock preservation across savepoints in PostgreSQL 9.3+. Prior releases failed to preserve FOR UPDATE locks after ROLLBACK TO, which has been fixed.

```sql
BEGIN;
SELECT * FROM mytable WHERE key = 1 FOR UPDATE;
SAVEPOINT s;
UPDATE mytable SET ... WHERE key = 1;
ROLLBACK TO s;
```

--------------------------------

### SSL Library Initialization

Source: https://www.postgresql.org/docs/current/bookindex.html

Functions for initializing SSL/TLS support in libpq.

```APIDOC
## SSL Library Initialization

### Overview
Functions for initializing SSL/TLS support.

### Functions

- **PQinitSSL** - Initializes SSL support
- **PQinitOpenSSL** - Initializes OpenSSL support
```

--------------------------------

### Example Usage of PostgreSQL to_tsvector

Source: https://www.postgresql.org/docs/current/textsearch-controls.html

This example demonstrates how `to_tsvector` processes a text string, showing tokenization, lexeme reduction, and stop word removal using the 'english' configuration.

```SQL
SELECT to_tsvector('english', 'a fat  cat sat on a mat - it ate a fat rats');
                  to_tsvector
-----------------------------------------------------
 'ate':9 'cat':3 'fat':2,11 'mat':7 'rat':12 'sat':4
```

--------------------------------

### PL/Tcl Transaction Management Example

Source: https://www.postgresql.org/docs/current/pltcl-transactions.html

This example demonstrates how to use `commit` and `rollback` within a PL/Tcl procedure. It inserts data into `test1` and commits or rolls back based on a condition.

```sql
CREATE PROCEDURE transaction_test1()
LANGUAGE pltcl
AS $$
for {set i 0} {$i < 10} {incr i} {
    spi_exec "INSERT INTO test1 (a) VALUES ($i)"
    if {$i % 2 == 0} {
        commit
    } else {
        rollback
    }
}
$$;

CALL transaction_test1();
```

--------------------------------

### Configure PostgreSQL Standby Server Parameters

Source: https://www.postgresql.org/docs/current/warm-standby.html

This snippet shows an example configuration for a PostgreSQL standby server, including connection details to the primary, a command for restoring WAL files from an archive, and a command for cleaning up old archive files.

```PostgreSQL Configuration
primary_conninfo = 'host=192.168.1.50 port=5432 user=foo password=foopass options=''-c wal_sender_timeout=5000'''
restore_command = 'cp /path/to/archive/%f %p'
archive_cleanup_command = 'pg_archivecleanup /path/to/archive %r'
```

--------------------------------

### EXECUTE IMMEDIATE Synopsis

Source: https://www.postgresql.org/docs/current/ecpg-sql-execute-immediate.html

Basic syntax for the EXECUTE IMMEDIATE command.

```sql
EXECUTE IMMEDIATE _string_
```

--------------------------------

### Server Options Configuration

Source: https://www.postgresql.org/docs/current/libpq-connect.html

Specifies command-line options to send to the PostgreSQL server at connection start. Options are space-separated and can be escaped with backslashes.

```APIDOC
## options

### Description
Specifies command-line options to send to the server at connection start.

### Parameter
- **options** (string) - Optional - Command-line options for the server

### Format
- Spaces within this string are considered to separate command-line arguments, unless escaped with a backslash (`\`)
- Write `\\` to represent a literal backslash

### Examples
- `-c geqo=off` - Sets the session's value of the `geqo` parameter to `off`
- `--geqo=off` - Alternative syntax for setting the `geqo` parameter

### Notes
For a detailed discussion of the available options, consult Chapter 19 of the PostgreSQL documentation.
```

--------------------------------

### CopyOutResponse (B) - Start Copy Out

Source: https://www.postgresql.org/docs/current/protocol-message-formats.html

Sent by the backend to indicate the start of a COPY OUT operation. This message will be followed by copy-out data. Specifies the overall copy format and format codes for each column.

```APIDOC
## CopyOutResponse (B)

### Description
Identifies the message as a Start Copy Out response. This message will be followed by copy-out data.

### Message Format

| Field | Type | Description |
|-------|------|-------------|
| Message Type | Byte1 | 'H' - Identifies the message as a Start Copy Out response |
| Length | Int32 | Length of message contents in bytes, including self |
| Format | Int8 | 0 = textual format (rows separated by newlines, columns by separator); 1 = binary format (similar to DataRow format) |
| Column Count | Int16 | The number of columns in the data to be copied (N) |
| Format Codes | Int16[N] | The format codes for each column. Each must be 0 (text) or 1 (binary). All must be 0 if overall copy format is textual |

### Notes
- Format code 0 indicates text format
- Format code 1 indicates binary format
- All format codes must be 0 if the overall copy format is textual
```

--------------------------------

### Create test table and insert XML documents

Source: https://www.postgresql.org/docs/current/xml2.html

Set up a test table with XML content for xpath_table demonstrations. Creates a table with an integer primary key and text column containing XML documents.

```SQL
CREATE TABLE test (
    id int PRIMARY KEY,
    xml text
);

INSERT INTO test VALUES (1, '<doc num="C1">
<line num="L1"><a>1</a><b>2</b><c>3</c></line>
<line num="L2"><a>11</a><b>22</b><c>33</c></line>
</doc>');

INSERT INTO test VALUES (2, '<doc num="C2">
<line num="L1"><a>111</a><b>222</b><c>333</c></line>
<line num="L2"><a>111</a><b>222</b><c>333</c></line>
</doc>');
```

--------------------------------

### Call URL Parsing Function

Source: https://www.postgresql.org/docs/current/plpgsql-porting.html

Example query demonstrating how to invoke the cs_parse_url function with a sample URL.

```sql
SELECT * FROM cs_parse_url('http://foobar.com/query.cgi?baz');
```

--------------------------------

### PostgreSQL CREATE TABLE AS Syntax

Source: https://www.postgresql.org/docs/current/sql-createtableas.htm

This snippet shows the complete syntax for the `CREATE TABLE AS` command in PostgreSQL, illustrating all available clauses and options for defining a new table from a query's results.

```sql
CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] _table_name_
    [ (_column_name_ [, ...] ) ]
    [ USING _method_ ]
    [ WITH ( _storage_parameter_ [= _value_] [, ... ] ) | WITHOUT OIDS ]
    [ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
    [ TABLESPACE _tablespace_name_ ]
    AS _query_
    [ WITH [ NO ] DATA ]
```

--------------------------------

### Example: Pass-by-Value Function (add_one)

Source: https://www.postgresql.org/docs/current/xfunc-c.html

Demonstrates a simple version-1 function that takes an int32 argument and returns an int32 result. This example shows the basic structure for pass-by-value data types.

```APIDOC
## Pass-by-Value Function Example

### Description
Simple function that increments an int32 value by 1.

### Function Name
add_one

### Implementation
```c
#include "postgres.h"
#include "fmgr.h"

PG_MODULE_MAGIC;
PG_FUNCTION_INFO_V1(add_one);

Datum
add_one(PG_FUNCTION_ARGS)
{
    int32   arg = PG_GETARG_INT32(0);
    PG_RETURN_INT32(arg + 1);
}
```

### Parameters
- **arg** (int32) - Required - The input value to increment

### Return Value
- **int32** - The input value incremented by 1

### Notes
- This is a pass-by-value function since int32 is a fixed-size scalar type
- The PG_GETARG_INT32 and PG_RETURN_INT32 macros handle the Datum conversion automatically
- No null checking is performed (assumes strict function)
```

--------------------------------

### Create a foreign table as a partition in PostgreSQL

Source: https://www.postgresql.org/docs/current/sql-createforeigntable.html

This example shows how to create a foreign table `measurement_y2016m07` that serves as a partition for an existing partitioned table `measurement`.

```SQL
CREATE FOREIGN TABLE measurement_y2016m07
    PARTITION OF measurement FOR VALUES FROM ('2016-07-01') TO ('2016-08-01')
    SERVER server_07;
```

--------------------------------

### psql Information and Help Options

Source: https://www.postgresql.org/docs/current/app-psql.htm

Command-line options for displaying version information and help documentation. These options provide access to psql reference materials.

```APIDOC
## Information and Help Options

### -V / --version
**Description**: Print the psql version and exit.
**Usage**: `psql -V`

### -? / --help[=topic]
**Description**: Show help about psql and exit.
**Optional Parameter**: `topic` (defaults to `options`)
**Available Topics**:
  - `commands`: Describes psql's backslash commands
  - `options`: Describes the command-line options that can be passed to psql
  - `variables`: Shows help about psql configuration variables
**Usage**: `psql -?` or `psql --help=commands`
```

--------------------------------

### DESCRIBE Command Synopsis

Source: https://www.postgresql.org/docs/current/ecpg-sql-describe.html

Illustrates the various syntaxes for the DESCRIBE command, including options for specifying output and descriptor types.

```SQL
DESCRIBE [ OUTPUT ] _prepared_name_ USING [ SQL ] DESCRIPTOR _descriptor_name_
DESCRIBE [ OUTPUT ] _prepared_name_ INTO [ SQL ] DESCRIPTOR _descriptor_name_
DESCRIBE [ OUTPUT ] _prepared_name_ INTO _sqlda_name_
```

--------------------------------

### DROP CAST Example - Remove Text to Integer Cast

Source: https://www.postgresql.org/docs/current/sql-dropcast.html

Example of dropping a cast from text type to int type. This removes the previously defined conversion between these two data types.

```sql
DROP CAST (text AS int);
```

--------------------------------

### CREATE SCHEMA equivalent multi-statement approach

Source: https://www.postgresql.org/docs/current/sql-createschema.html

Demonstrates the equivalent way to create a schema with objects using separate statements instead of nested subcommands. Each statement is independent and fully qualified.

```SQL
CREATE SCHEMA hollywood;
CREATE TABLE hollywood.films (title text, release date, awards text[]);
CREATE VIEW hollywood.winners AS
    SELECT title, release FROM hollywood.films WHERE awards IS NOT NULL;
```

--------------------------------

### ALTER OPERATOR FAMILY - ADD Example

Source: https://www.postgresql.org/docs/current/sql-alteropfamily.html

Practical example demonstrating how to add cross-data-type operators and support functions to an existing B-tree operator family for int4 and int2 data types.

```APIDOC
## ALTER OPERATOR FAMILY - ADD

### Description
Adds operators and support functions to an existing operator family. This example demonstrates adding cross-data-type operators and support functions to a B-tree operator family.

### Example
The following command adds cross-data-type operators and support functions to an operator family that already contains B-tree operator classes for data types int4 and int2:

```sql
ALTER OPERATOR FAMILY integer_ops USING btree ADD

  -- int4 vs int2
  OPERATOR 1 < (int4, int2) ,
  OPERATOR 2 <= (int4, int2) ,
  OPERATOR 3 = (int4, int2) ,
  OPERATOR 4 >= (int4, int2) ,
  OPERATOR 5 > (int4, int2) ,
  FUNCTION 1 btint42cmp(int4, int2) ,

  -- int2 vs int4
  OPERATOR 1 < (int2, int4) ,
  OPERATOR 2 <= (int2, int4) ,
  OPERATOR 3 = (int2, int4) ,
  OPERATOR 4 >= (int2, int4) ,
  OPERATOR 5 > (int2, int4) ,
  FUNCTION 1 btint24cmp(int2, int4) ;
```

### Explanation
- **integer_ops**: The name of the operator family being modified
- **btree**: The index method
- **OPERATOR clauses**: Define comparison operators for cross-data-type operations (int4 vs int2 and int2 vs int4)
- **FUNCTION clauses**: Associate support functions (btint42cmp and btint24cmp) with the operators
- **Strategy numbers**: 1-5 represent <, <=, =, >=, > operators respectively in B-tree
```

--------------------------------

### Execute SQL queries in psql

Source: https://www.postgresql.org/docs/current/tutorial-accessdb.html

These examples demonstrate how to execute basic SQL queries within the `psql` interactive terminal. The output for each query is displayed directly below the command.

```sql
mydb=> SELECT version();
                                         version
-------------------------------------------------------------------​-----------------------
 PostgreSQL 18.3 on x86_64-pc-linux-gnu, compiled by gcc (Debian 4.9.2-10) 4.9.2, 64-bit
(1 row)

mydb=> SELECT current_date;
    date
------------
 2016-01-07
(1 row)

mydb=> SELECT 2 + 2;
 ?column?
----------
        4
(1 row)
```

--------------------------------

### Collation Version Mismatch Warning Example

Source: https://www.postgresql.org/docs/current/sql-altercollation.html

Example warning message issued when a collation's recorded version differs from the current system version, typically after OS or library upgrades.

```SQL
WARNING:  collation "xx-x-icu" has version mismatch
DETAIL:  The collation in the database was created using version 1.2.3.4, but the operating system provides version 2.3.4.5.
HINT:  Rebuild all objects affected by this collation and run ALTER COLLATION pg_catalog."xx-x-icu" REFRESH VERSION, or build PostgreSQL with the right library version.
```

--------------------------------

### Create table with array column in PostgreSQL

Source: https://www.postgresql.org/docs/current/ecpg-variables.html

Example table structure and data for demonstrating array handling in ECPG.

```SQL
CREATE TABLE t3 (
    ii integer[]
);

testdb=> SELECT * FROM t3;
     ii
-------------
 {1,2,3,4,5}
(1 row)
```

--------------------------------

### Initialize OpenSSL Library with PQinitOpenSSL (C)

Source: https://www.postgresql.org/docs/current/libpq-ssl.html

This function allows applications to indicate that `libssl` and/or `libcrypto` libraries have been initialized. It is deprecated and does nothing in modern PostgreSQL versions.

```C
void PQinitOpenSSL(int do_ssl, int do_crypto);
```

--------------------------------

### Create a database with createdb

Source: https://www.postgresql.org/docs/current/tutorial-createdb.html

Use the createdb utility to create a new database. If no name is provided, it defaults to the current user name.

```shell
$ **createdb mydb**
```

```shell
$ **createdb**
```

--------------------------------

### Date format mask and input examples

Source: https://www.postgresql.org/docs/current/ecpg-pgtypes.html

Examples of valid input formats and strings demonstrating how the function extracts date components. The function can handle extra text and non-standard delimiters.

```text
(ddd) mmm. dd, yyyy | (Mon) Nov. 23, 1959
```

```text
ddmmyy | 21-2-54 | 1954-02-21
```

```text
ddmmyy | 2-12-54 | 1954-12-02
```

```text
ddmmyy | 20111954 | 1954-11-20
```

```text
ddmmyy | 130464 | 1964-04-13
```

```text
mmm.dd.yyyy | MAR-12-1967 | 1967-03-12
```

```text
yy/mm/dd | 1954, February 3rd | 1954-02-03
```

```text
mmm.dd.yyyy | 041269 | 1969-04-12
```

```text
yy/mm/dd | In the year 2525, in the month of July, mankind will be alive on the 28th day | 2525-07-28
```

```text
dd-mm-yy | I said on the 28th of July in the year 2525 | 2525-07-28
```

```text
mmm.dd.yyyy | 9/14/58 | 1958-09-14
```

```text
yy/mm/dd | 47/03/29 | 1947-03-29
```

```text
mmm.dd.yyyy | oct 28 1975 | 1975-10-28
```

```text
mmddyy | Nov 14th, 1985 | 1985-11-14
```

--------------------------------

### Example of ALLOCATE DESCRIPTOR in Embedded SQL

Source: https://www.postgresql.org/docs/current/ecpg-sql-allocate-descriptor.html

This example demonstrates how to allocate an SQL descriptor area named 'mydesc' using the `EXEC SQL` directive, typical for embedded SQL applications.

```sql
EXEC SQL ALLOCATE DESCRIPTOR mydesc;
```

--------------------------------

### Create Database Locally using createdb

Source: https://www.postgresql.org/docs/current/app-createdb.htm

Creates a new PostgreSQL database named `demo` on the default local server instance.

```bash
$ **createdb demo**
```

--------------------------------

### Get default connection options with PQconndefaults

Source: https://www.postgresql.org/docs/current/libpq-connect.html

Returns an array of PQconninfoOption structures; the returned memory must be freed using PQconninfoFree.

```C
PQconninfoOption *PQconndefaults(void);

typedef struct
{
    char   *keyword;   /* The keyword of the option */
    char   *envvar;    /* Fallback environment variable name */
    char   *compiled;  /* Fallback compiled in default value */
    char   *val;       /* Option's current value, or NULL */
    char   *label;     /* Label for field in connect dialog */
    char   *dispchar;  /* Indicates how to display this field
                          in a connect dialog. Values are:
                          ""        Display entered value as is
                          "*"       Password field - hide value
                          "D"       Debug option - don't show by default */
    int     dispsize;  /* Field size in characters for dialog */
} PQconninfoOption;
```

--------------------------------

### pg_createsubscriber Command Reference

Source: https://www.postgresql.org/docs/current/app-pgcreatesubscriber.html

Complete reference for the pg_createsubscriber command-line utility, including its synopsis, required options, and usage patterns for converting physical replicas to logical replicas.

```APIDOC
## pg_createsubscriber

### Description
pg_createsubscriber converts a physical replica into a new logical replica. It creates a pair of publication and subscription objects for each database and must be run at the target server.

### Command
pg_createsubscriber

### Synopsis
```
pg_createsubscriber [option...] {-d | --database} dbname {-D | --pgdata} datadir {-P | --publisher-server} connstr
```

### Required Options
- **-d, --database** (string) - Required - The name of the database to convert to logical replica
- **-D, --pgdata** (string) - Required - The data directory path of the target server
- **-P, --publisher-server** (string) - Required - Connection string to the publisher server

### Behavior
- Creates a new logical replica from a physical standby server
- Includes all tables in the specified database in the logical replication setup
- Creates a pair of publication and subscription objects for each database
- Does not copy initial table data; performs only the synchronization phase
- Brings each table to a synchronized state
- Results in a state analogous to a fresh logical replication setup

### Use Cases
- Optimized for large database systems where initial data copy is time-consuming
- Reduces the time spent on data synchronization compared to standard logical replication setup
- Minimizes the amount of changes to be applied during replica availability

### Notes
- For smaller databases, standard logical replication with initial data synchronization is recommended
- Refer to the CREATE SUBSCRIPTION copy_data option for additional details on data synchronization options
```

--------------------------------

### Run PostgreSQL Regression Tests Against Existing Installation (Parallel)

Source: https://www.postgresql.org/docs/current/regress-run.html

This command executes the regression tests in parallel against an existing and running PostgreSQL installation. It requires the server to be active and a data directory initialized.

```bash
make installcheck-parallel
```

--------------------------------

### Example: Variable-Length Data Function (copytext)

Source: https://www.postgresql.org/docs/current/xfunc-c.html

Demonstrates a version-1 function that works with variable-length data types (text). This example shows handling of variable-length headers, memory allocation, and data copying.

```APIDOC
## Variable-Length Data Function Example

### Description
Function that creates a copy of a text value, handling variable-length headers and data.

### Function Name
copytext

### Implementation
```c
#include "varatt.h"

PG_FUNCTION_INFO_V1(copytext);

Datum
copytext(PG_FUNCTION_ARGS)
{
    text     *t = PG_GETARG_TEXT_PP(0);

    /*
     * VARSIZE_ANY_EXHDR is the size of the struct in bytes, minus the
     * VARHDRSZ or VARHDRSZ_SHORT of its header.  Construct the copy with a
     * full-length header.
     */
    text     *new_t = (text *) palloc(VARSIZE_ANY_EXHDR(t) + VARHDRSZ);
    SET_VARSIZE(new_t, VARSIZE_ANY_EXHDR(t) + VARHDRSZ);

    /*
     * VARDATA is a pointer to the data region of the new struct.  The source
     * could be a short datum, so retrieve its data through VARDATA_ANY.
     */
    memcpy(VARDATA(new_t),          /* destination */
           VARDATA_ANY(t),          /* source */
           VARSIZE_ANY_EXHDR(t));   /* how many bytes */
    PG_RETURN_TEXT_P(new_t);
}
```

### Parameters
- **t** (text*) - Required - The text value to copy

### Return Value
- **text*** - A new text value that is a copy of the input

### Key Macros
- **PG_GETARG_TEXT_PP(n)** - Retrieves text argument, handling both short and long datums
- **VARSIZE_ANY_EXHDR(t)** - Gets size of data excluding header
- **VARHDRSZ** - Size of full-length variable-length header
- **SET_VARSIZE(ptr, size)** - Sets the size field in variable-length header
- **VARDATA(ptr)** - Pointer to data region of new struct
- **VARDATA_ANY(ptr)** - Pointer to data region, handles both short and long datums

### Notes
- Requires inclusion of varatt.h header
- Uses palloc for memory allocation
- Handles both short and long datum formats
- Constructs copy with full-length header
- Uses memcpy to copy the actual data bytes
```

--------------------------------

### PL/Perl Transaction Control Example

Source: https://www.postgresql.org/docs/current/plperl-builtins.html

This example demonstrates explicit transaction management within a PL/Perl procedure using `spi_commit()` and `spi_rollback()`. It inserts data and commits or rolls back based on a condition.

```plperl
CREATE PROCEDURE transaction_test1()
LANGUAGE plperl
AS $$
foreach my $i (0..9) {
    spi_exec_query("INSERT INTO test1 (a) VALUES ($i)");
    if ($i % 2 == 0) {
        spi_commit();
    } else {
        spi_rollback();
    }
}
$$;
```

```sql
CALL transaction_test1();
```

--------------------------------

### Create Function and Execute Query

Source: https://www.postgresql.org/docs/current/rules-privileges.html

This example shows the creation of a PostgreSQL function and a query that uses it. The planner may execute the inexpensive function before the WHERE clause condition, potentially revealing data that the view was intended to hide.

```sql
CREATE FUNCTION tricky(text, text) RETURNS bool AS $$
BEGIN
    RAISE NOTICE "% => %", $1, $2;
    RETURN true;
END;
$$ LANGUAGE plpgsql COST 0.0000000000000000000001;

SELECT * FROM phone_number WHERE tricky(person, phone);
```

--------------------------------

### PostgreSQL Replication Conflict Error Log Example

Source: https://www.postgresql.org/docs/current/logical-replication-conflicts.html

Example error message logged when a replication conflict is detected, showing the conflict type, constraint details, and transaction information needed for resolution.

```text
ERROR:  conflict detected on relation "public.test": conflict=insert_exists
DETAIL:  Key already exists in unique index "t_pkey", which was modified locally in transaction 740 at 2024-06-26 10:47:04.727375+08.
Key (c)=(1); existing local row (1, 'local'); remote row (1, 'remote').
CONTEXT:  processing remote data for replication origin "pg_16395" during "INSERT" for replication target relation "public.test" in transaction 725 finished at 0/14C0378
```

--------------------------------

### Retrieve live connection options with PQconninfo

Source: https://www.postgresql.org/docs/current/libpq-connect.html

Returns the connection options and values used for an active PGconn object.

```C
PQconninfoOption *PQconninfo(PGconn *conn);
```

--------------------------------

### Run pgbench Benchmark Test

Source: https://www.postgresql.org/docs/current/pgbench.html

Executes a pgbench benchmark against the specified database after initialization. Key options include `-c` for number of clients, `-t` for transactions, `-T` for time limit, and `-f` for custom script files.

```bash
pgbench [ _options_ ] _dbname_
```

--------------------------------

### Row constructor comparison syntax and example

Source: https://www.postgresql.org/docs/current/functions-comparisons.html

Compares two row constructors field by field. The example shows that comparison stops at the first unequal pair, even if subsequent fields are NULL.

```sql
_row_constructor_ _operator_ _row_constructor_\n
```

```sql
ROW(1,2,NULL) < ROW(1,3,0)
```

--------------------------------

### Create and verify base backup with pg_verifybackup

Source: https://www.postgresql.org/docs/current/app-pgverifybackup.html

Create a base backup from a remote server and verify its integrity using pg_verifybackup on the backup directory.

```bash
$ pg_basebackup -h mydbserver -D /usr/local/pgsql/data
$ pg_verifybackup /usr/local/pgsql/data
```

--------------------------------

### CASE Expression with Table Query Example

Source: https://www.postgresql.org/docs/current/functions-conditional.html

Practical example showing CASE used to transform numeric values into text labels. Demonstrates conditional evaluation with multiple WHEN clauses and ELSE fallback.

```SQL
SELECT * FROM test;

 a
---
 1
 2
 3


SELECT a,
       CASE WHEN a=1 THEN 'one'
            WHEN a=2 THEN 'two'
            ELSE 'other'
       END
    FROM test;

 a | case
---+-------
 1 | one
 2 | two
 3 | other
```

--------------------------------

### Basic Transaction Control in PL/pgSQL Procedures

Source: https://www.postgresql.org/docs/current/plpgsql-transactions.html

Use COMMIT and ROLLBACK within a loop to manage transaction boundaries. A new transaction starts automatically after each command without a separate START TRANSACTION call.

```sql
CREATE PROCEDURE transaction_test1()
LANGUAGE plpgsql
AS $$
BEGIN
    FOR i IN 0..9 LOOP
        INSERT INTO test1 (a) VALUES (i);
        IF i % 2 = 0 THEN
            COMMIT;
        ELSE
            ROLLBACK;
        END IF;
    END LOOP;
END;
$$;

CALL transaction_test1();
```

--------------------------------

### Start PostgreSQL with External Log Rotation using rotatelogs

Source: https://www.postgresql.org/docs/current/logfile-maintenance.html

This command pipes the pg_ctl output to rotatelogs for external log management. It starts the PostgreSQL server and rotates logs daily (86400 seconds).

```shell
pg_ctl start | rotatelogs /var/log/pgsql_log 86400
```

--------------------------------

### psql Variable and Configuration Options

Source: https://www.postgresql.org/docs/current/app-psql.htm

Command-line options for setting variables, managing configuration files, and controlling startup behavior. These options allow customization of psql behavior at invocation time.

```APIDOC
## Variable and Configuration Options

### -v assignment / --set=assignment / --variable=assignment
**Description**: Perform a variable assignment, like the `\set` meta-command.
**Syntax**: Separate name and value by an equal sign on the command line.
**Special Cases**:
  - To unset a variable: leave off the equal sign
  - To set a variable with an empty value: use the equal sign but leave off the value
**Timing**: Assignments are done during command line processing, so variables that reflect connection state will get overwritten later.
**Usage**: `psql -v var_name=value [connection_options]`

### -X / --no-psqlrc
**Description**: Do not read the start-up file (neither the system-wide `psqlrc` file nor the user's `~/.psqlrc` file).
**Usage**: `psql -X [connection_options]`
```

--------------------------------

### Use sqlda_t for dynamic SQL in ECPG

Source: https://www.postgresql.org/docs/current/ecpg-informix-compat.html

Demonstrates preparing a statement, describing it into an SQLDA, and fetching results using the descriptor.

```c
EXEC SQL INCLUDE sqlda.h;

    sqlda_t        *sqlda; /* This doesn't need to be under embedded DECLARE SECTION */

    EXEC SQL BEGIN DECLARE SECTION;
    char *prep_stmt = "select * from table1";
    int i;
    EXEC SQL END DECLARE SECTION;

    ...

    EXEC SQL PREPARE mystmt FROM :prep_stmt;

    EXEC SQL DESCRIBE mystmt INTO sqlda;

    printf("# of fields: %d\n", sqlda->sqld);
    for (i = 0; i < sqlda->sqld; i++)
      printf("field %d: \"%s\"\n", sqlda->sqlvar[i]->sqlname);

    EXEC SQL DECLARE mycursor CURSOR FOR mystmt;
    EXEC SQL OPEN mycursor;
    EXEC SQL WHENEVER NOT FOUND GOTO out;

    while (1)
    {
      EXEC SQL FETCH mycursor USING sqlda;
    }

    EXEC SQL CLOSE mycursor;

    free(sqlda); /* The main structure is all to be free(),
                  * sqlda and sqlda->sqlvar is in one allocated area */
```

--------------------------------

### Example Output from crosstab Query

Source: https://www.postgresql.org/docs/current/tablefunc.html

Shows the resulting table structure when using crosstab with a defined set of output columns.

```Text
           <== value  columns  ==>
 row_name   category_1   category_2
----------+------------+------------
  row1        val1         val2
  row2        val5         val6
```

--------------------------------

### Use array get to return composite type in PL/Tcl

Source: https://www.postgresql.org/docs/current/pltcl-functions.html

The Tcl array get command converts an array representation into a list suitable for returning as a composite type. Useful for modifying and returning structured data.

```sql
CREATE FUNCTION raise_pay(employee, delta int) RETURNS employee AS $$
    set 1(salary) [expr {$1(salary) + $2}]
    return [array get 1]
$$ LANGUAGE pltcl;
```

--------------------------------

### normal_rand Query Example

Source: https://www.postgresql.org/docs/current/tablefunc.html

Example query generating 1000 normally distributed random values with mean 5 and standard deviation 3. Shows typical output format with multiple rows of float values.

```SQL
test=# SELECT * FROM normal_rand(1000, 5, 3);
     normal_rand
----------------------
     1.56556322244898
     9.10040991424657
     5.36957140345079
   -0.369151492880995
    0.283600703686639
       .
       .
       .
     4.82992125404908
     9.71308014517282
     2.49639286969028
(1000 rows)
```

--------------------------------

### Event Trigger Example: DDL Command Logger

Source: https://www.postgresql.org/docs/current/pltcl-event-trigger.html

A practical example of an event trigger function in PL/Tcl that logs DDL command execution by raising a NOTICE message containing the event name and command tag.

```APIDOC
## Event Trigger Example: DDL Command Logger

### Description
This example demonstrates a simple event trigger function that logs each DDL command execution by raising a NOTICE message with the event type and command tag.

### Function Definition
```sql
CREATE OR REPLACE FUNCTION tclsnitch() RETURNS event_trigger AS $$
  elog NOTICE "tclsnitch: $TG_event $TG_tag"
$$ LANGUAGE pltcl;
```

### Trigger Creation
```sql
CREATE EVENT TRIGGER tcl_a_snitch ON ddl_command_start EXECUTE FUNCTION tclsnitch();
```

### Behavior
- Fires on: `ddl_command_start` event
- Action: Raises a NOTICE message
- Message Format: "tclsnitch: [event_name] [command_tag]"
- Example Output: "tclsnitch: ddl_command_start CREATE TABLE"

### Variables Used
- **$TG_event** - Contains the event name (e.g., "ddl_command_start")
- **$TG_tag** - Contains the command tag (e.g., "CREATE TABLE")
```

--------------------------------

### Generating Constant Tables and UNION Equivalence

Source: https://www.postgresql.org/docs/current/queries-values.html

A basic VALUES list example and its equivalent representation using SELECT and UNION ALL.

```sql
VALUES (1, 'one'), (2, 'two'), (3, 'three');
```

```sql
SELECT 1 AS column1, 'one' AS column2
UNION ALL
SELECT 2, 'two'
UNION ALL
SELECT 3, 'three';
```

--------------------------------

### Displaying access privileges with psql \dp

Source: https://www.postgresql.org/docs/current/ddl-priv.html

Example output of the psql \dp command showing the resulting access and column privileges after GRANT operations.

```psql
=> \dp mytable
                                  Access privileges
 Schema |  Name   | Type  |   Access privileges    |   Column privileges   | Policies
--------+---------+-------+------------------------+-----------------------+----------
 public | mytable | table | miriam=arwdDxtm/miriam+|
        |         |       | =r/miriam             +|
        |         |       | admin=arw/miriam       |
(1 row)

```

--------------------------------

### Sample Makefile for PGXS Extension

Source: https://www.postgresql.org/docs/current/extend-pgxs.html

A standard Makefile for an extension module. The variables define the module name, extension metadata, and files to be installed.

```makefile
MODULES = isbn_issn
EXTENSION = isbn_issn
DATA = isbn_issn--1.0.sql
DOCS = README.isbn_issn
HEADERS_isbn_issn = isbn_issn.h

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)

```

--------------------------------

### Initial Query Tree for shoe_ready View

Source: https://www.postgresql.org/docs/current/rules-views.html

Represents the parser output before any rules are applied to the shoe_ready view.

```sql
SELECT shoe_ready.shoename, shoe_ready.sh_avail,
       shoe_ready.sl_name, shoe_ready.sl_avail,
       shoe_ready.total_avail
  FROM shoe_ready shoe_ready
 WHERE shoe_ready.total_avail >= 2;
```

--------------------------------

### dblink_build_sql_delete Usage Example

Source: https://www.postgresql.org/docs/current/contrib-dblink-build-sql-delete.html

Example demonstrating how to call dblink_build_sql_delete with a mixed-case table name and primary key values. The function generates a DELETE statement that targets rows matching the specified primary key values.

```sql
SELECT dblink_build_sql_delete('"MyFoo"', '1 2', 2, '{"1", "b"}');
           dblink_build_sql_delete
---------------------------------------------
 DELETE FROM "MyFoo" WHERE f1='1' AND f2='b'
(1 row)
```

--------------------------------

### GET version()

Source: https://www.postgresql.org/docs/current/functions-info.html

Returns a string describing the PostgreSQL server's version. Developers should use `server_version_num` or `PQserverVersion` for machine-readable versions.

```APIDOC
## GET version()

### Description
Returns a string describing the PostgreSQL server's version. You can also get this information from server_version, or for a machine-readable version use server_version_num. Software developers should use `server_version_num` (available since 8.2) or `PQserverVersion` instead of parsing the text version.

### Method
GET

### Endpoint
version()

### Parameters

### Request Example

### Response
#### Success Response (200)
- **text** (string) - The PostgreSQL server's version string.

#### Response Example
```
"PostgreSQL 16.2 (Debian 16.2-1.pgdg120+2)"
```
```

--------------------------------

### Control Greediness in PostgreSQL regexp_match for Substring Extraction

Source: https://www.postgresql.org/docs/current/functions-matching.html

These examples illustrate how different greediness settings for `.*` and the overall RE affect `regexp_match` results. The final example shows how to force overall greediness to achieve the desired capture groups.

```SQL
SELECT regexp_match('abc01234xyz', '(.*)(\d+)(.*)');
```

```SQL
SELECT regexp_match('abc01234xyz', '(.*?)(\d+)(.*)');
```

```SQL
SELECT regexp_match('abc01234xyz', '(?:(.*?)(\d+)(.*)){1,1}');
```

--------------------------------

### Implementing Triggered Change Notifications (tcn)

Source: https://www.postgresql.org/docs/current/tcn.html

This example shows how to set up a table, define the tcn trigger, and observe the asynchronous notification payloads for INSERT, UPDATE, and DELETE operations.

```sql
test=# create table tcndata
test-#   (
test(#     a int not null,
test(#     b date not null,
test(#     c text,
test(#     primary key (a, b)
test(#   );
CREATE TABLE
test=# create trigger tcndata_tcn_trigger
test-#   after insert or update or delete on tcndata
test-#   for each row execute function triggered_change_notification();
CREATE TRIGGER
test=# listen tcn;
LISTEN
test=# insert into tcndata values (1, date '2012-12-22', 'one'),
test-#                            (1, date '2012-12-23', 'another'),
test-#                            (2, date '2012-12-23', 'two');
INSERT 0 3
Asynchronous notification "tcn" with payload ""tcndata",I,"a"='1',"b"='2012-12-22'" received from server process with PID 22770.
Asynchronous notification "tcn" with payload ""tcndata",I,"a"='1',"b"='2012-12-23'" received from server process with PID 22770.
Asynchronous notification "tcn" with payload ""tcndata",I,"a"='2',"b"='2012-12-23'" received from server process with PID 22770.
test=# update tcndata set c = 'uno' where a = 1;
UPDATE 2
Asynchronous notification "tcn" with payload ""tcndata",U,"a"='1',"b"='2012-12-22'" received from server process with PID 22770.
Asynchronous notification "tcn" with payload ""tcndata",U,"a"='1',"b"='2012-12-23'" received from server process with PID 22770.
test=# delete from tcndata where a = 1 and b = date '2012-12-22';
DELETE 1
Asynchronous notification "tcn" with payload ""tcndata",D,"a"='1',"b"='2012-12-22'" received from server process with PID 22770.

```

--------------------------------

### PQprepare

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Submits a request to create a prepared statement with the given parameters, and waits for completion. This feature allows commands to be executed repeatedly without being parsed and planned each time.

```APIDOC
## PQprepare

### Description
Submits a request to create a prepared statement with the given parameters, and waits for completion. This feature allows commands to be executed repeatedly without being parsed and planned each time; see PREPARE for details.

### Method
Function Call

### Signature
PGresult *PQprepare(PGconn *conn,
                    const char *stmtName,
                    const char *query,
                    int nParams,
                    const Oid *paramTypes);

### Parameters
- **conn** (PGconn *) - Connection object.
- **stmtName** (const char *) - Name of the prepared statement. Can be "" to create an unnamed statement, in which case any pre-existing unnamed statement is automatically replaced.
- **query** (const char *) - The SQL command string, which must contain a single SQL command.
- **nParams** (int) - The number of parameters for which types are pre-specified in the array paramTypes[].
- **paramTypes** (const Oid *) - An array of OIDs specifying the data types to be assigned to the parameter symbols. If NULL, or any particular element in the array is zero, the server assigns a data type to the parameter symbol.

### Return Value
- **PGresult *** (PGresult *) - A PGresult object whose contents indicate server-side success or failure. A null result indicates out-of-memory or inability to send the command at all.
```

--------------------------------

### Example: Pass-by-Reference Composite Type Function (makepoint)

Source: https://www.postgresql.org/docs/current/xfunc-c.html

Demonstrates a version-1 function that works with composite types (Point). This example shows explicit pointer handling for pass-by-reference data types and memory allocation using palloc.

```APIDOC
## Pass-by-Reference Composite Type Example

### Description
Function that creates a new Point by combining the x-coordinate from one point and y-coordinate from another.

### Function Name
makepoint

### Implementation
```c
#include "utils/geo_decls.h"

PG_FUNCTION_INFO_V1(makepoint);

Datum
makepoint(PG_FUNCTION_ARGS)
{
    /* Here, the pass-by-reference nature of Point is not hidden. */
    Point     *pointx = PG_GETARG_POINT_P(0);
    Point     *pointy = PG_GETARG_POINT_P(1);
    Point     *new_point = (Point *) palloc(sizeof(Point));

    new_point->x = pointx->x;
    new_point->y = pointy->y;

    PG_RETURN_POINT_P(new_point);
}
```

### Parameters
- **pointx** (Point*) - Required - First point (x-coordinate used)
- **pointy** (Point*) - Required - Second point (y-coordinate used)

### Return Value
- **Point*** - New Point with x from first argument and y from second argument

### Notes
- Uses PG_GETARG_POINT_P to retrieve pointers to Point structures
- Memory for the new point is allocated using palloc (PostgreSQL memory allocator)
- PG_RETURN_POINT_P returns the pointer to the newly allocated Point
- The pass-by-reference nature is explicit in this example (pointer handling is visible)
- Requires inclusion of utils/geo_decls.h header
```

--------------------------------

### Intended Usage of Variadic Aggregate with ORDER BY

Source: https://www.postgresql.org/docs/current/xaggr.htm

This example clarifies the correct syntax for passing multiple arguments to a variadic aggregate before an `ORDER BY` clause.

```SQL
SELECT myaggregate(a, b, c ORDER BY a) FROM ...
```

--------------------------------

### PL/pgSQL RETURN Examples for Scalar and Composite Types

Source: https://www.postgresql.org/docs/current/plpgsql-control-structures.html

These examples illustrate returning scalar values (literals, variables) and composite (row) types from PL/pgSQL functions. Note the requirement for explicit casting when returning composite types.

```sql
-- functions returning a scalar type
RETURN 1 + 2;
RETURN scalar_var;

-- functions returning a composite type
RETURN composite_type_var;
RETURN (1, 2, 'three'::text);  -- must cast columns to correct types
```

--------------------------------

### Examples of WHENEVER actions

Source: https://www.postgresql.org/docs/current/ecpg-sql-whenever.html

Various ways to handle NOT FOUND, SQLWARNING, and SQLERROR conditions using built-in actions or custom functions.

```sql
EXEC SQL WHENEVER NOT FOUND CONTINUE;
EXEC SQL WHENEVER NOT FOUND DO BREAK;
EXEC SQL WHENEVER NOT FOUND DO CONTINUE;
EXEC SQL WHENEVER SQLWARNING SQLPRINT;
EXEC SQL WHENEVER SQLWARNING DO warn();
EXEC SQL WHENEVER SQLERROR sqlprint;
EXEC SQL WHENEVER SQLERROR CALL print2();
EXEC SQL WHENEVER SQLERROR DO handle_error("select");
EXEC SQL WHENEVER SQLERROR DO sqlnotice(NULL, NONO);
EXEC SQL WHENEVER SQLERROR DO sqlprint();
EXEC SQL WHENEVER SQLERROR GOTO error_label;
EXEC SQL WHENEVER SQLERROR STOP;
```

--------------------------------

### Setup Foreign Data Wrapper and Materialized View for Spell Check

Source: https://www.postgresql.org/docs/current/rules-materializedviews.html

Configures 'file_fdw' to access a dictionary file, creates a foreign table, and then creates a materialized view 'wrd' with indexes for efficient spell-checking.

```SQL
CREATE EXTENSION file_fdw;
CREATE SERVER local_file FOREIGN DATA WRAPPER file_fdw;
CREATE FOREIGN TABLE words (word text NOT NULL)
  SERVER local_file
  OPTIONS (filename '/usr/share/dict/words');
CREATE MATERIALIZED VIEW wrd AS SELECT * FROM words;
CREATE UNIQUE INDEX wrd_word ON wrd (word);
CREATE EXTENSION pg_trgm;
CREATE INDEX wrd_trgm ON wrd USING gist (word gist_trgm_ops);
VACUUM ANALYZE wrd;
```

--------------------------------

### regexp_replace() with start position and case-insensitive flag

Source: https://www.postgresql.org/docs/current/functions-matching.html

Specify a start position and use the 'i' flag for case-insensitive matching; the N parameter controls which match to replace (0 or omitted replaces first, greater than 0 replaces the Nth match).

```SQL
regexp_replace('A PostgreSQL function', 'a|e|i|o|u', 'X', 1, 0, 'i')
```

--------------------------------

### SPI_commit - Commit Current Transaction

Source: https://www.postgresql.org/docs/current/spi-spi-commit.html

Commits the current transaction in an SPI connection. After commit, a new transaction is automatically started with default characteristics. If commit fails, the transaction is rolled back and a new transaction is started before the error is thrown.

```APIDOC
## SPI_commit

### Description
Commits the current transaction. Approximately equivalent to running the SQL command `COMMIT`. After the transaction is committed, a new transaction is automatically started using default transaction characteristics, so that the caller can continue using SPI facilities. If there is a failure during commit, the current transaction is instead rolled back and a new transaction is started, after which the error is thrown in the usual way.

### Signature
```c
void SPI_commit(void)
```

### Parameters
None

### Requirements
- The SPI connection must be set as nonatomic in the call to `SPI_connect_ext`

### Behavior
- Commits the current transaction
- Automatically starts a new transaction with default characteristics
- On failure: rolls back current transaction, starts new transaction, then throws error

### Related Functions
- `SPI_commit_and_chain` - Commit with same transaction characteristics
- `SPI_rollback` - Rollback the current transaction
```

--------------------------------

### Demonstrate Multi-Column Exclusion Constraint (PostgreSQL)

Source: https://www.postgresql.org/docs/current/rangetypes.html

Illustrates insertions into the `room_reservation` table, showing how the multi-column exclusion constraint works for different rooms and overlapping times.

```sql
INSERT INTO room_reservation VALUES
    ('123A', '[2010-01-01 14:00, 2010-01-01 15:00)');
```

```sql
INSERT INTO room_reservation VALUES
    ('123A', '[2010-01-01 14:30, 2010-01-01 15:30)');
```

```sql
INSERT INTO room_reservation VALUES
    ('123B', '[2010-01-01 14:30, 2010-01-01 15:30)');
```

--------------------------------

### Add Tables to a Publication

Source: https://www.postgresql.org/docs/current/sql-alterpublication.html

This example demonstrates how to add one or more tables to an existing publication, optionally specifying a subset of columns for a table.

```SQL
ALTER PUBLICATION mypublication ADD TABLE users (user_id, firstname), departments;

```

--------------------------------

### Create Table with Composite Primary Key and Query dblink_get_pkey

Source: https://www.postgresql.org/docs/current/contrib-dblink-get-pkey.html

Example demonstrating creation of a table with a multi-column primary key and retrieval of primary key information using dblink_get_pkey.

```sql
CREATE TABLE foobar (
    f1 int,
    f2 int,
    f3 int,
    PRIMARY KEY (f1, f2, f3)
);
CREATE TABLE

SELECT * FROM dblink_get_pkey('foobar');
 position | colname
----------+---------
        1 | f1
        2 | f2
        3 | f3
(3 rows)
```

--------------------------------

### CopyInResponse (B) - Start Copy In

Source: https://www.postgresql.org/docs/current/protocol-message-formats.html

Sent by the backend to indicate the start of a COPY IN operation. The frontend must respond with copy-in data or send a CopyFail message. Specifies the overall copy format (textual or binary) and the format codes for each column.

```APIDOC
## CopyInResponse (B)

### Description
Identifies the message as a Start Copy In response. The frontend must now send copy-in data (if not prepared to do so, send a CopyFail message).

### Message Format

| Field | Type | Description |
|-------|------|-------------|
| Message Type | Byte1 | 'G' - Identifies the message as a Start Copy In response |
| Length | Int32 | Length of message contents in bytes, including self |
| Format | Int8 | 0 = textual format (rows separated by newlines, columns by separator); 1 = binary format (similar to DataRow format) |
| Column Count | Int16 | The number of columns in the data to be copied (N) |
| Format Codes | Int16[N] | The format codes for each column. Each must be 0 (text) or 1 (binary). All must be 0 if overall copy format is textual |

### Notes
- Format code 0 indicates text format
- Format code 1 indicates binary format
- All format codes must be 0 if the overall copy format is textual
```

--------------------------------

### Build PDF documentation using Make

Source: https://www.postgresql.org/docs/current/docguide-build.html

Generates PDF files using FOP. Select the target based on the required paper size.

```shell
doc/src/sgml$ **make postgres-A4.pdf**

```

```shell
doc/src/sgml$ **make postgres-US.pdf**

```

--------------------------------

### CALLBACK startup_cb

Source: https://www.postgresql.org/docs/current/logicaldecoding-output-plugin.html

An optional callback invoked when a replication slot is created or starts streaming. It is used to initialize the plugin state and configure output options.

```APIDOC
## CALLBACK startup_cb

### Description
The optional startup_cb callback is called whenever a replication slot is created or asked to stream changes, independent of the number of changes ready to be put out.

### Method
LogicalDecodeStartupCB

### Endpoint
startup_cb

### Parameters
#### Path Parameters
- **ctx** (struct LogicalDecodingContext*) - Required - The logical decoding context.
- **options** (OutputPluginOptions*) - Required - Struct of options that output plugins can set, such as output_type and receive_rewrites.
- **is_init** (bool) - Required - True when the replication slot is being created, false otherwise.

### Request Example
```c
typedef void (*LogicalDecodeStartupCB) (struct LogicalDecodingContext *ctx,
                                        OutputPluginOptions *options,
                                        bool is_init);
```

### Response
#### Success Response (void)
- **void** - No return value expected.
```

--------------------------------

### C Program Demonstrating CONNECT with Host Variables

Source: https://www.postgresql.org/docs/current/ecpg-sql-connect.html

An example C program that uses embedded SQL to connect to a PostgreSQL database, demonstrating how to use host variables for database name, user, and connection string.

```c
int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    char *dbname     = "testdb";    /* database name */
    char *user       = "testuser";  /* connection user name */
    char *connection = "tcp:postgresql://localhost:5432/testdb";
                                    /* connection string */
    char ver[256];                  /* buffer to store the version string */
EXEC SQL END DECLARE SECTION;

    ECPGdebug(1, stderr);

    EXEC SQL CONNECT TO :dbname USER :user;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL SELECT version() INTO :ver;
    EXEC SQL DISCONNECT;

    printf("version: %s\n", ver);

    EXEC SQL CONNECT TO :connection USER :user;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL SELECT version() INTO :ver;
    EXEC SQL DISCONNECT;

    printf("version: %s\n", ver);

    return 0;
}
```

--------------------------------

### PL/pgSQL Assignment Examples

Source: https://www.postgresql.org/docs/current/plpgsql-statements.html

Practical examples of variable assignments including scalar values, record fields, array elements, and array slices. Type coercion is automatic; if no direct cast exists, textual conversion is attempted via output and input functions.

```sql
tax := subtotal * 0.06;
my_record.user_id := 20;
my_array[j] := 20;
my_array[1:3] := array[1,2,3];
complex_array[n].realpart = 12.3;
```

--------------------------------

### Create synonym dictionary with configuration file

Source: https://www.postgresql.org/docs/current/textsearch-dictionaries.html

Creates a synonym dictionary named 'syn' using the synonym_sample.syn configuration file. The SYNONYMS parameter specifies the base name of the configuration file located in $SHAREDIR/tsearch_data/.

```SQL
CREATE TEXT SEARCH DICTIONARY syn (template=synonym, synonyms='synonym_sample');
```

--------------------------------

### Destroy a PostgreSQL Database with Specific Host, Port, and Interactive Confirmation

Source: https://www.postgresql.org/docs/current/app-dropdb.htm

This example demonstrates how to drop a database on a remote server, specifying host and port. It includes interactive confirmation and echoes the underlying SQL command.

```bash
$ **dropdb -p 5000 -h eden -i -e demo**
Database "demo" will be permanently deleted.
Are you sure? (y/n) **y**
DROP DATABASE demo;
```

--------------------------------

### NUMERIC Type Declaration Examples

Source: https://www.postgresql.org/docs/current/datatype-numeric.html

Examples of NUMERIC column declarations with different precision and scale values. NUMERIC(3,1) stores values between -99.9 and 99.9; NUMERIC(2,-3) rounds to nearest thousand; NUMERIC(3,5) stores fractional values between -0.00999 and 0.00999.

```SQL
NUMERIC(3, 1)
```

```SQL
NUMERIC(2, -3)
```

```SQL
NUMERIC(3, 5)
```

--------------------------------

### Get string length with length

Source: https://www.postgresql.org/docs/current/functions-string.html

Returns the number of characters in the string.

```SQL
length('jose')
```

--------------------------------

### DROP SUBSCRIPTION example

Source: https://www.postgresql.org/docs/current/sql-dropsubscription.html

Drops a subscription named 'mysub' from the database.

```sql
DROP SUBSCRIPTION mysub;
```

--------------------------------

### Example source_sql Query Result

Source: https://www.postgresql.org/docs/current/tablefunc.html

Illustrates the expected output format for the `source_sql` parameter, including `row_name`, `extra_col`, `cat`, and `value` columns.

```SQL
SELECT row_name, extra_col, cat, value FROM foo ORDER BY 1;

 row_name    extra_col   cat    value
----------+------------+-----+---------
  row1         extra1    cat1    val1
  row1         extra1    cat2    val2
  row1         extra1    cat4    val4
  row2         extra2    cat1    val5
  row2         extra2    cat2    val6
  row2         extra2    cat3    val7
  row2         extra2    cat4    val8
```

--------------------------------

### CALLBACK begin_cb

Source: https://www.postgresql.org/docs/current/logicaldecoding-output-plugin.html

A required callback invoked when the start of a committed transaction has been decoded.

```APIDOC
## CALLBACK begin_cb

### Description
The required begin_cb callback is called whenever a start of a committed transaction has been decoded. Aborted transactions are never decoded.

### Method
LogicalDecodeBeginCB

### Endpoint
begin_cb

### Parameters
#### Path Parameters
- **ctx** (struct LogicalDecodingContext*) - Required - The logical decoding context.
- **txn** (ReorderBufferTXN*) - Required - Contains meta information about the transaction, such as commit timestamp and XID.

### Request Example
```c
typedef void (*LogicalDecodeBeginCB) (struct LogicalDecodingContext *ctx,
                                      ReorderBufferTXN *txn);
```

### Response
#### Success Response (void)
- **void** - No return value expected.
```

--------------------------------

### Convert PostgreSQL record to hstore

Source: https://www.postgresql.org/docs/current/hstore.html

Demonstrates how to create a table, insert data, and then convert a table row (record) into an hstore representation.

```sql
CREATE TABLE test (col1 integer, col2 text, col3 text);
INSERT INTO test VALUES (123, 'foo', 'bar');

SELECT hstore(t) FROM test AS t;
```

--------------------------------

### Partial Update Example for Substitution Context

Source: https://www.postgresql.org/docs/current/rules-update.html

A partial snippet illustrating an alternative update that would affect how the rule system performs substitutions.

```sql
UPDATE shoelace_data SET sl_color = 'green'
```

--------------------------------

### Enable and Observe JIT with EXPLAIN ANALYZE in PostgreSQL

Source: https://www.postgresql.org/docs/current/jit-decision.html

Adjust `jit_above_cost` to a lower value to enable JIT compilation for queries with a lower estimated cost. This example demonstrates how JIT details appear in the `EXPLAIN ANALYZE` output.

```sql
=# SET jit_above_cost = 10;
SET
=# EXPLAIN ANALYZE SELECT SUM(relpages) FROM pg_class;
                                                 QUERY PLAN
-------------------------------------------------------------------​------------------------------------------
 Aggregate  (cost=16.27..16.29 rows=1 width=8) (actual time=6.049..6.049 rows=1.00 loops=1)
   Buffers: shared hit=14
   ->  Seq Scan on pg_class  (cost=0.00..15.42 rows=342 width=4) (actual time=0.019..0.052 rows=356.00 loops=1)
         Buffers: shared hit=14
 Planning Time: 0.133 ms
 JIT:
   Functions: 3
   Options: Inlining false, Optimization false, Expressions true, Deforming true
   Timing: Generation 1.259 ms (Deform 0.000 ms), Inlining 0.000 ms, Optimization 0.797 ms, Emission 5.048 ms, Total 7.104 ms
 Execution Time: 7.416 ms
```

--------------------------------

### Get column count with PQnfields

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Returns the number of fields in each row of the result.

```c
int PQnfields(const PGresult *res);
```

--------------------------------

### Allow MD5 and SCRAM Authentication for Domain

Source: https://www.postgresql.org/docs/current/auth-pg-hba-conf.html

This pair of entries allows connections from hosts within the '.example.com' domain. It uses MD5 authentication for the user 'mike' and SCRAM-SHA-256 for all other users, accommodating older clients.

```postgresql
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             mike            .example.com            md5
host    all             all             .example.com            scram-sha-256
```

--------------------------------

### Get row count with PQntuples

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Returns the number of rows in the PGresult object.

```c
int PQntuples(const PGresult *res);
```

--------------------------------

### GET unicode_version()

Source: https://www.postgresql.org/docs/current/functions-info.html

Returns a string representing the version of Unicode used by PostgreSQL.

```APIDOC
## GET unicode_version()

### Description
Returns a string representing the version of Unicode used by PostgreSQL.

### Method
GET

### Endpoint
unicode_version()

### Parameters

### Request Example

### Response
#### Success Response (200)
- **text** (string) - The Unicode version string.

#### Response Example
```
"15.0"
```
```

--------------------------------

### pg_combinebackup Version and Help Options

Source: https://www.postgresql.org/docs/current/app-pgcombinebackup.html

Command line options for displaying version information and help documentation for pg_combinebackup. These options provide quick access to utility information and command syntax.

```APIDOC
## pg_combinebackup Command Line Options

### Description
Command line options for the pg_combinebackup utility to display version information and help documentation.

### Options

#### Version Option
- **-V** - Prints the pg_combinebackup version and exits.
- **--version** - Prints the pg_combinebackup version and exits.

#### Help Options
- **-?** - Shows help about pg_combinebackup command line arguments, and exits.
- **--help** - Shows help about pg_combinebackup command line arguments, and exits.
```

--------------------------------

### Get client encoding with pg_client_encoding

Source: https://www.postgresql.org/docs/current/functions-string.html

Returns the name of the current client encoding.

```sql
pg_client_encoding()
```

--------------------------------

### Define OAuth Validator Startup Callback in C

Source: https://www.postgresql.org/docs/current/oauth-validator-callbacks.html

This callback is executed immediately after the module loads. It is used for initial setup and state storage within `state->private_data`.

```c
typedef void (*ValidatorStartupCB) (ValidatorModuleState *state);
```

--------------------------------

### Get length of bytea in SQL

Source: https://www.postgresql.org/docs/current/functions-binarystring.html

Returns the number of bytes in the binary string.

```SQL
length('\x1234567890'::bytea)
```

--------------------------------

### Initialize Build Directory

Source: https://www.postgresql.org/docs/current/install-meson.html

Creates and configures the mandatory build directory for the project.

```shell
**meson setup build**


```

--------------------------------

### GET enum_last (anyenum)

Source: https://www.postgresql.org/docs/current/functions-enum.html

Returns the last value of the input enum type.

```APIDOC
## GET enum_last (anyenum)

### Description
This function returns the last value of the specified enum type.

### Method
N/A (SQL Function)

### Endpoint
N/A (SQL Function)

### Parameters
#### Request Body
- **anyenum** (anyenum) - Required - An instance of the enum type (can be NULL) to determine the enum type.

### Request Example
N/A

### Response
#### Success Response (200)
- **result** (anyenum) - The last value of the enum type.

#### Response Example
```
enum_last(null::rainbow) → purple
```
```

--------------------------------

### Create RANGE partitions for year-month measurement table

Source: https://www.postgresql.org/docs/current/sql-createtable.htm

Creates multiple RANGE partitions for a measurement_year_month table with year and month columns as partition keys. Each partition covers a specific month range.

```SQL
CREATE TABLE measurement_ym_y2016m11
    PARTITION OF measurement_year_month
    FOR VALUES FROM (2016, 11) TO (2016, 12);
```

```SQL
CREATE TABLE measurement_ym_y2016m12
    PARTITION OF measurement_year_month
    FOR VALUES FROM (2016, 12) TO (2017, 01);
```

```SQL
CREATE TABLE measurement_ym_y2017m01
    PARTITION OF measurement_year_month
    FOR VALUES FROM (2017, 01) TO (2017, 02);
```

--------------------------------

### GET enum_first (anyenum)

Source: https://www.postgresql.org/docs/current/functions-enum.html

Returns the first value of the input enum type.

```APIDOC
## GET enum_first (anyenum)

### Description
This function returns the first value of the specified enum type.

### Method
N/A (SQL Function)

### Endpoint
N/A (SQL Function)

### Parameters
#### Request Body
- **anyenum** (anyenum) - Required - An instance of the enum type (can be NULL) to determine the enum type.

### Request Example
N/A

### Response
#### Success Response (200)
- **result** (anyenum) - The first value of the enum type.

#### Response Example
```
enum_first(null::rainbow) → red
```
```

--------------------------------

### SELECT * FROM pg_settings

Source: https://www.postgresql.org/docs/current/view-pg-settings.html

Retrieves a comprehensive list of all run-time configuration parameters for the PostgreSQL server.

```APIDOC
## SELECT * FROM pg_settings

### Description
The view pg_settings provides access to run-time parameters of the server. It is essentially an alternative interface to the SHOW and SET commands. It also provides access to some facts about each parameter that are not directly available from SHOW, such as minimum and maximum values.

### Method
SELECT

### Endpoint
pg_settings

### Parameters
#### Query Parameters
- **name** (text) - Optional - Filter by the specific configuration parameter name.

### Response
#### Success Response (200)
- **name** (text) - Run-time configuration parameter name
- **setting** (text) - Current value of the parameter
- **unit** (text) - Implicit unit of the parameter
- **category** (text) - Logical group of the parameter
- **short_desc** (text) - A brief description of the parameter
- **extra_desc** (text) - Additional, more detailed, description of the parameter
- **context** (text) - Context required to set the parameter's value (internal, postmaster, sighup, superuser-backend, backend, superuser, user)
- **vartype** (text) - Parameter type (bool, enum, integer, real, or string)
- **source** (text) - Source of the current parameter value
- **min_val** (text) - Minimum allowed value of the parameter (null for non-numeric values)
- **max_val** (text) - Maximum allowed value of the parameter (null for non-numeric values)
- **enumvals** (text[]) - Allowed values of an enum parameter (null for non-enum values)
- **boot_val** (text) - Parameter value assumed at server startup if the parameter is not otherwise set
- **reset_val** (text) - Value that RESET would reset the parameter to in the current session
- **sourcefile** (text) - Configuration file the current value was set in
- **sourceline** (int4) - Line number within the configuration file the current value was set at
- **pending_restart** (bool) - True if the value has been changed in the configuration file but needs a restart

#### Response Example
{
  "name": "max_connections",
  "setting": "100",
  "unit": null,
  "category": "Connections and Authentication / Connection Settings",
  "short_desc": "Sets the maximum number of concurrent connections.",
  "extra_desc": null,
  "context": "postmaster",
  "vartype": "integer",
  "source": "configuration file",
  "min_val": "1",
  "max_val": "262143",
  "enumvals": null,
  "boot_val": "100",
  "reset_val": "100",
  "sourcefile": "/var/lib/postgresql/data/postgresql.conf",
  "sourceline": 64,
  "pending_restart": false
}
```

--------------------------------

### Drop a publication

Source: https://www.postgresql.org/docs/current/sql-droppublication.html

A basic example of removing a specific publication named mypublication.

```sql
DROP PUBLICATION mypublication;

```

--------------------------------

### USING Clause Shorthand

Source: https://www.postgresql.org/docs/current/queries-table-expressions.html

Example of how the USING shorthand translates into an explicit ON condition.

```sql
USING (a, b)
```

```sql
ON _`T1`_.a =_`T2`_.a AND _`T1`_.b =_`T2`_.b
```

--------------------------------

### PostgreSQL Service File Configuration Example

Source: https://www.postgresql.org/docs/current/libpq-pgservice.html

INI-format service file defining connection parameters for a named service. Place in ~/.pg_service.conf (Unix/Linux/macOS) or %APPDATA%\postgresql\.pg_service.conf (Windows), or specify custom path via PGSERVICEFILE environment variable.

```ini
# comment
[mydb]
host=somehost
port=5433
user=admin
```

--------------------------------

### Create a basic PostgreSQL user

Source: https://www.postgresql.org/docs/current/app-createuser.htm

Use `createuser` to quickly create a new role with default settings on the default database server.

```bash
$ **createuser joe**
```

--------------------------------

### Configure basic_archive in postgresql.conf

Source: https://www.postgresql.org/docs/current/basic-archive.html

Enable WAL archiving and specify the target directory for segment files. The directory must exist prior to starting the server.

```ini
# postgresql.conf
archive_mode = 'on'
archive_library = 'basic_archive'
basic_archive.archive_directory = '/path/to/archive/directory'

```

--------------------------------

### CALLBACK begin_prepare_cb

Source: https://www.postgresql.org/docs/current/logicaldecoding-output-plugin.html

Required callback called whenever the start of a prepared transaction has been decoded.

```APIDOC
## CALLBACK begin_prepare_cb

### Description
The required begin_prepare_cb callback is called whenever the start of a prepared transaction has been decoded.

### Method
CALLBACK

### Endpoint
begin_prepare_cb

### Parameters
#### Function Parameters
- **ctx** (struct LogicalDecodingContext *) - Required - The decoding context.
- **txn** (ReorderBufferTXN *) - Required - The transaction being prepared.

### Request Example
```c
typedef void (*LogicalDecodeBeginPrepareCB) (struct LogicalDecodingContext *ctx, ReorderBufferTXN *txn);
```
```

--------------------------------

### Connect, prepare statement, and declare cursor

Source: https://www.postgresql.org/docs/current/ecpg-descriptors.html

Establish a database connection, prepare a parameterized SQL query that joins pg_database and pg_stat_database, and declare a cursor for the prepared statement.

```C
int
main(void)
{
    EXEC SQL BEGIN DECLARE SECTION;
    char query[1024] = "SELECT d.oid,* FROM pg_database d, pg_stat_database s WHERE d.oid=s.datid AND ( d.datname=? OR d.oid=? )";
    EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO testdb AS con1 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    EXEC SQL PREPARE stmt1 FROM :query;
    EXEC SQL DECLARE cur1 CURSOR FOR stmt1;
```

--------------------------------

### FUNCTION amrescan

Source: https://www.postgresql.org/docs/current/index-functions.html

Starts or restarts an index scan, potentially with new scan keys.

```APIDOC
## FUNCTION amrescan

### Description
Start or restart an index scan, possibly with new scan keys. Used when a new outer tuple is selected by a nested-loop join.

### Method
FUNCTION

### Endpoint
amrescan

### Parameters
#### Path Parameters
- **scan** (IndexScanDesc) - Required - The scan descriptor to restart.
- **keys** (ScanKey) - Optional - New scan keys (NULL to use previous).
- **nkeys** (int) - Required - Number of keys.
- **orderbys** (ScanKey) - Optional - New ordering operators (NULL to use previous).
- **norderbys** (int) - Required - Number of ordering operators.
```

--------------------------------

### Create weather table with basic SQL types

Source: https://www.postgresql.org/docs/current/tutorial-table.html

Creates a table with varchar, int, real, and date columns. Use this as a basic template for table creation; note that comments use -- syntax and the semicolon terminates the command.

```SQL
CREATE TABLE weather (
    city            varchar(80),
    temp_lo         int,           -- low temperature
    temp_hi         int,           -- high temperature
    prcp            real,          -- precipitation
    date            date
);
```

--------------------------------

### Check string prefix in PostgreSQL

Source: https://www.postgresql.org/docs/current/functions-string.html

Returns true if the string starts with the specified prefix.

```sql
starts_with('alphabet', 'alph')
```

--------------------------------

### SPI_cursor_open_with_paramlist Function

Source: https://www.postgresql.org/docs/current/spi-spi-cursor-open-with-paramlist.html

Sets up a cursor using a prepared statement and parameter list. This function is equivalent to SPI_cursor_open but accepts parameter information in ParamListInfo format, which is convenient for passing values already available in that structure and supports dynamic parameter sets via hook functions.

```APIDOC
## SPI_cursor_open_with_paramlist

### Description
Sets up a cursor (internally, a portal) that will execute a statement prepared by SPI_prepare. This function is equivalent to SPI_cursor_open except that information about the parameter values to be passed to the query is presented differently. The ParamListInfo representation can be convenient for passing down values that are already available in that format. It also supports use of dynamic parameter sets via hook functions specified in ParamListInfo. The passed-in parameter data will be copied into the cursor's portal, so it can be freed while the cursor still exists.

### Signature
```c
Portal SPI_cursor_open_with_paramlist(const char *name,
                                      SPIPlanPtr plan,
                                      ParamListInfo params,
                                      bool read_only)
```

### Parameters

#### Function Arguments
- **name** (const char *) - Optional - Name for portal, or NULL to let the system select a name
- **plan** (SPIPlanPtr) - Required - Prepared statement returned by SPI_prepare
- **params** (ParamListInfo) - Optional - Data structure containing parameter types and values; NULL if none
- **read_only** (bool) - Required - true for read-only execution

### Return Value
- **Portal** - Pointer to portal containing the cursor. Note there is no error return convention; any error will be reported via elog.
```

--------------------------------

### Get source table OID with PQftable

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Returns the OID of the table from which the column was fetched.

```c
Oid PQftable(const PGresult *res,
             int column_number);
```

--------------------------------

### PostgreSQL Foreign Data Wrapper Server and User Setup

Source: https://www.postgresql.org/docs/current/contrib-dblink-connect.html

Creates a Foreign Data Wrapper server, user, and user mapping for dblink connections. Non-superuser connections require password authentication; SCRAM pass-through is not supported for local connections.

```SQL
CREATE SERVER fdtest FOREIGN DATA WRAPPER dblink_fdw OPTIONS (hostaddr '127.0.0.1', dbname 'contrib_regression');

CREATE USER regress_dblink_user WITH PASSWORD 'secret';
CREATE USER MAPPING FOR regress_dblink_user SERVER fdtest OPTIONS (user 'regress_dblink_user', password 'secret');
GRANT USAGE ON FOREIGN SERVER fdtest TO regress_dblink_user;
GRANT SELECT ON TABLE foo TO regress_dblink_user;
```

--------------------------------

### Get tsvector length

Source: https://www.postgresql.org/docs/current/functions-textsearch.html

Returns the total number of lexemes present within a tsvector.

```SQL
length('fat:2,4 cat:3 rat:5A'::tsvector)
```

--------------------------------

### GET enum_range (anyenum)

Source: https://www.postgresql.org/docs/current/functions-enum.html

Returns all values of the input enum type in an ordered array.

```APIDOC
## GET enum_range (anyenum)

### Description
This function returns all values of the specified enum type as an ordered array.

### Method
N/A (SQL Function)

### Endpoint
N/A (SQL Function)

### Parameters
#### Request Body
- **anyenum** (anyenum) - Required - An instance of the enum type (can be NULL) to determine the enum type.

### Request Example
N/A

### Response
#### Success Response (200)
- **result** (anyarray) - An ordered array containing all values of the enum type.

#### Response Example
```
enum_range(null::rainbow) → {red,orange,yellow,green,blue,purple}
```
```

--------------------------------

### Define a SETOF Function with Output Parameters

Source: https://www.postgresql.org/docs/current/xfunc-sql.html

This example shows how to create a set-returning function that uses OUT parameters and returns SETOF record when multiple output parameters are defined.

```SQL
CREATE TABLE tab (y int, z int);
INSERT INTO tab VALUES (1, 2), (3, 4), (5, 6), (7, 8);

CREATE FUNCTION sum_n_product_with_tab (x int, OUT sum int, OUT product int)
RETURNS SETOF record
AS $$
    SELECT $1 + tab.y, $1 * tab.y FROM tab;
$$ LANGUAGE SQL;

SELECT * FROM sum_n_product_with_tab(10);
```

--------------------------------

### Get octet length of bytea in SQL

Source: https://www.postgresql.org/docs/current/functions-binarystring.html

Returns the number of bytes in the binary string.

```SQL
octet_length('\x123456'::bytea)
```

--------------------------------

### pgbench Option: -C / --connect

Source: https://www.postgresql.org/docs/current/pgbench.html

Establishes a new database connection for each transaction, rather than reusing a single connection per client session. Useful for measuring connection overhead.

```APIDOC
## COMMAND-LINE OPTION -C / --connect

### Description
Instructs pgbench to establish a new connection for each transaction, instead of connecting only once per client session. This option is useful for measuring the overhead associated with establishing database connections.

### Method
Command-line argument

### Endpoint
pgbench

### Parameters
#### Path Parameters
- No path parameters.

#### Query Parameters
- No query parameters.

#### Request Body
- No request body. This is a flag option.

### Request Example
```bash
pgbench -C
pgbench --connect
```

### Response
#### Success Response (0)
- No direct API response. The option modifies pgbench's connection behavior.

#### Response Example
No direct API response.
```

--------------------------------

### Get Number of Cube Dimensions in PostgreSQL

Source: https://www.postgresql.org/docs/current/cube.html

Returns the number of dimensions of a given cube.

```sql
cube_dim('(1,2),(3,4)')
```

--------------------------------

### Install hstore extension into a specific schema

Source: https://www.postgresql.org/docs/current/sql-createextension.html

Demonstrates two methods for specifying the target schema for an extension's objects. Ensure the target schema is secure to prevent unauthorized privilege escalation.

```sql
CREATE EXTENSION hstore SCHEMA addons;

```

```sql
SET search_path = addons;
CREATE EXTENSION hstore;

```

--------------------------------

### GET /pg_conversion

Source: https://www.postgresql.org/docs/current/catalog-pg-conversion.html

Retrieves metadata about encoding conversion functions from the pg_conversion system catalog.

```APIDOC
## GET /pg_conversion\n\n### Description\nThe catalog pg_conversion describes encoding conversion functions. It is used to identify the function to call for converting between different character set encodings.\n\n### Method\nGET\n\n### Endpoint\npg_conversion\n\n### Parameters\n- **oid** (oid) - Required - Row identifier\n- **conname** (name) - Required - Conversion name (unique within a namespace)\n- **connamespace** (oid) - Required - The OID of the namespace that contains this conversion\n- **conowner** (oid) - Required - Owner of the conversion\n- **conforencoding** (int4) - Required - Source encoding ID\n- **contoencoding** (int4) - Required - Destination encoding ID\n- **conproc** (regproc) - Required - Conversion function\n- **condefault** (bool) - Required - True if this is the default conversion\n\n### Request Example\nSELECT * FROM pg_conversion WHERE conname = 'utf8_to_ascii';\n\n### Response\n#### Success Response (200)\n- **oid** (oid) - Row identifier\n- **conname** (name) - Conversion name\n- **connamespace** (oid) - Namespace OID\n- **conowner** (oid) - Owner OID\n- **conforencoding** (int4) - Source encoding ID\n- **contoencoding** (int4) - Destination encoding ID\n- **conproc** (regproc) - Conversion function OID\n- **condefault** (bool) - Default flag\n\n### Response Example\n{\n  "oid": 12345,\n  "conname": "utf8_to_ascii",\n  "connamespace": 11,\n  "conowner": 10,\n  "conforencoding": 6,\n  "contoencoding": 0,\n  "conproc": "utf8_to_ascii_proc",\n  "condefault": true\n}
```

--------------------------------

### Connect to PostgreSQL with service and SSL mode

Source: https://www.postgresql.org/docs/current/app-psql.htm

Use a conninfo string to specify connection parameters including service name and SSL requirements. This provides an alternative to individual command-line options.

```bash
$ psql "service=myservice sslmode=require"
```

--------------------------------

### Rename a PostgreSQL Conversion

Source: https://www.postgresql.org/docs/current/sql-alterconversion.html

Example demonstrating how to rename an existing conversion from 'iso_8859_1_to_utf8' to 'latin1_to_unicode'.

```SQL
ALTER CONVERSION iso_8859_1_to_utf8 RENAME TO latin1_to_unicode;
```

--------------------------------

### Explain a Simple Query Plan in PostgreSQL

Source: https://www.postgresql.org/docs/current/sql-explain.htm

Use EXPLAIN to view the execution plan for a basic SELECT query on a table.

```sql
EXPLAIN SELECT * FROM foo;

                       QUERY PLAN
---------------------------------------------------------
 Seq Scan on foo  (cost=0.00..155.00 rows=10000 width=4)
(1 row)
```

--------------------------------

### PostgreSQL string_to_array Function Example

Source: https://www.postgresql.org/docs/current/release-8-0-9.html

Demonstrates the string_to_array function with overlapping separator characters.

```sql
string_to_array('123xx456xxx789', 'xx')
```

--------------------------------

### Deallocate a descriptor in Embedded SQL

Source: https://www.postgresql.org/docs/current/ecpg-sql-deallocate-descriptor.html

Example of deallocating a specific descriptor named mydesc.

```sql
EXEC SQL DEALLOCATE DESCRIPTOR mydesc;
```

--------------------------------

### Execute Prepared Statement with PQexecPrepared

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Sends a request to execute a previously prepared statement. This avoids re-parsing and re-planning the query for repeated executions.

```c
PGresult *PQexecPrepared(PGconn *conn,
                         const char *stmtName,
                         int nParams,
                         const char * const *paramValues,
                         const int *paramLengths,
                         const int *paramFormats,
                         int resultFormat);

```

--------------------------------

### Initial INSERT...SELECT Statement

Source: https://www.postgresql.org/docs/current/rules-update.html

The starting query that inserts all rows from shoelace_arrive into shoelace_ok.

```SQL
INSERT INTO shoelace_ok SELECT * FROM shoelace_arrive;
```

--------------------------------

### SPI_cursor_open_with_args

Source: https://www.postgresql.org/docs/current/spi-spi-cursor-open-with-args.html

Sets up a cursor (internally, a portal) that will execute the specified query with parameters. This function is now deprecated in favor of SPI_cursor_parse_open.

```APIDOC
## SPI_cursor_open_with_args

### Description
SPI_cursor_open_with_args sets up a cursor (internally, a portal) that will execute the specified query. Most of the parameters have the same meanings as the corresponding parameters to SPI_prepare_cursor and SPI_cursor_open.
For one-time query execution, this function should be preferred over SPI_prepare_cursor followed by SPI_cursor_open. If the same command is to be executed with many different parameters, either method might be faster, depending on the cost of re-planning versus the benefit of custom plans.
The passed-in parameter data will be copied into the cursor's portal, so it can be freed while the cursor still exists.
This function is now deprecated in favor of SPI_cursor_parse_open, which provides equivalent functionality using a more modern API for handling query parameters.

### Parameters
#### Request Body
- **_name_** (const char *) - Optional - name for portal, or NULL to let the system select a name
- **_command_** (const char *) - Required - command string
- **_nargs_** (int) - Required - number of input parameters ($1, $2, etc.)
- **_argtypes_** (Oid *) - Required - an array of length _nargs_, containing the OIDs of the data types of the parameters
- **_values_** (Datum *) - Required - an array of length _nargs_, containing the actual parameter values
- **_nulls_** (const char *) - Optional - an array of length _nargs_, describing which parameters are null. If _nulls_ is NULL then SPI_cursor_open_with_args assumes that no parameters are null. Otherwise, each entry of the _nulls_ array should be ' ' if the corresponding parameter value is non-null, or 'n' if the corresponding parameter value is null.
- **_read_only_** (bool) - Required - true for read-only execution
- **_cursorOptions_** (int) - Required - integer bit mask of cursor options; zero produces default behavior

### Response
#### Return Value
- **Portal** - Pointer to portal containing the cursor. Note there is no error return convention; any error will be reported via elog.
```

--------------------------------

### BASE_BACKUP

Source: https://www.postgresql.org/docs/current/protocol-replication.html

Instructs the server to start streaming a base backup, automatically managing backup mode.

```APIDOC
## BASE_BACKUP

### Description
Instructs the server to start streaming a base backup. The system will automatically be put in backup mode before the backup is started, and taken out of it when the backup is complete.

### Method
Command

### Endpoint
Not applicable (Backup command)

### Parameters
#### Query Parameters
- **LABEL** (string) - Required - The label for the backup.
- **option** (string) - Optional - Other options for the base backup.

### Request Example
```sql
BASE_BACKUP (LABEL 'my_full_backup')
```

### Response
#### Success Response
Server starts streaming the base backup data. The exact format of the streamed data is not detailed here but is implied to be the backup content itself.
```

--------------------------------

### PL/pgSQL RETURN NEXT and RETURN QUERY Syntax

Source: https://www.postgresql.org/docs/current/plpgsql-control-structures.html

Illustrates the basic syntax for RETURN NEXT, RETURN QUERY, and RETURN QUERY EXECUTE used in PL/pgSQL set-returning functions.

```sql
RETURN NEXT _expression_;
RETURN QUERY _query_;
RETURN QUERY EXECUTE _command-string_ [ USING _expression_ [, ... ] ];
```

--------------------------------

### SELECT current_time / current_timestamp

Source: https://www.postgresql.org/docs/current/functions-datetime.html

Functions to retrieve the current date and time at the start of the current transaction.

```APIDOC
## SELECT current_time / current_timestamp

### Description
Returns the current time or timestamp, optionally with a specified precision for fractional seconds.

### Method
SELECT

### Endpoint
current_time(integer), current_timestamp(integer)

### Parameters
#### Path Parameters
- **precision** (integer) - Optional - The number of fractional digits in the seconds field.

### Request Example
SELECT current_time(2);

### Response
#### Success Response (200)
- **result** (time with time zone / timestamp with time zone) - The current system time or timestamp.

#### Response Example
{
  "current_time": "14:39:53.66-05",
  "current_timestamp": "2019-12-23 14:39:53.662522-05"
}
```

--------------------------------

### Sample table by execution time

Source: https://www.postgresql.org/docs/current/tsm-system-time.html

Uses the SYSTEM_TIME method to read as many rows as possible within a 1000 millisecond (1 second) limit.

```sql
SELECT * FROM my_table TABLESAMPLE SYSTEM_TIME(1000);

```

--------------------------------

### PostgreSQL CREATE TABLE Synopsis

Source: https://www.postgresql.org/docs/current/sql-createtable.htm

This snippet provides the complete syntax for the CREATE TABLE command in PostgreSQL, covering standard tables, typed tables, and table partitions, along with various column and table constraints.

```SQL
CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] _table_name_ ( [
  { _column_name_ _data_type_ [ STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT } ] [ COMPRESSION _compression_method_ ] [ COLLATE _collation_ ] [ _column_constraint_ [ ... ] ]
    | _table_constraint_
    | LIKE _source_table_ [ _like_option_ ... ] }
    [, ... ]
] )
[ INHERITS ( _parent_table_ [, ... ] ) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { _column_name_ | ( _expression_ ) } [ COLLATE _collation_ ] [ _opclass_ ] [, ... ] ) ]
[ USING _method_ ]
[ WITH ( _storage_parameter_ [= _value_] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE _tablespace_name_ ]

CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] _table_name_
    OF _type_name_ [ (
  { _column_name_ [ WITH OPTIONS ] [ _column_constraint_ [ ... ] ]
    | _table_constraint_ }
    [, ... ]
) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { _column_name_ | ( _expression_ ) } [ COLLATE _collation_ ] [ _opclass_ ] [, ... ] ) ]
[ USING _method_ ]
[ WITH ( _storage_parameter_ [= _value_] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE _tablespace_name_ ]

CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] _table_name_
    PARTITION OF _parent_table_ [ (
  { _column_name_ [ WITH OPTIONS ] [ _column_constraint_ [ ... ] ]
    | _table_constraint_ }
    [, ... ]
) ] { FOR VALUES _partition_bound_spec_ | DEFAULT }
[ PARTITION BY { RANGE | LIST | HASH } ( { _column_name_ | ( _expression_ ) } [ COLLATE _collation_ ] [ _opclass_ ] [, ... ] ) ]
[ USING _method_ ]
[ WITH ( _storage_parameter_ [= _value_] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE _tablespace_name_ ]

where _column_constraint_ is:

[ CONSTRAINT _constraint_name_ ]
{ NOT NULL [ NO INHERIT ]  |
  NULL |
  CHECK ( _expression_ ) [ NO INHERIT ] |
  DEFAULT _default_expr_ |
  GENERATED ALWAYS AS ( _generation_expr_ ) [ STORED | VIRTUAL ] |
  GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( _sequence_options_ ) ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] _index_parameters_ |
  PRIMARY KEY _index_parameters_ |
  REFERENCES _reftable_ [ ( _refcolumn_ ) ] [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ]
    [ ON DELETE _referential_action_ ] [ ON UPDATE _referential_action_ ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ] [ ENFORCED | NOT ENFORCED ]

and _table_constraint_ is:

[ CONSTRAINT _constraint_name_ ]
{ CHECK ( _expression_ ) [ NO INHERIT ] |
  NOT NULL _column_name_ [ NO INHERIT ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] ( _column_name_ [, ... ] [, _column_name_ WITHOUT OVERLAPS ] ) _index_parameters_ |
  PRIMARY KEY ( _column_name_ [, ... ] [, _column_name_ WITHOUT OVERLAPS ] ) _index_parameters_ |
  EXCLUDE [ USING _index_method_ ] ( _exclude_element_ WITH _operator_ [, ... ] ) _index_parameters_ [ WHERE ( _predicate_ ) ] |
  FOREIGN KEY ( _column_name_ [, ... ] [, PERIOD _column_name_ ] ) REFERENCES _reftable_ [ ( _refcolumn_ [, ... ] [, PERIOD _refcolumn_ ] ) ]
    [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ] [ ON DELETE _referential_action_ ] [ ON UPDATE _referential_action_ ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ] [ ENFORCED | NOT ENFORCED ]

and _like_option_ is:

{ INCLUDING | EXCLUDING } { COMMENTS | COMPRESSION | CONSTRAINTS | DEFAULTS | GENERATED | IDENTITY | INDEXES | STATISTICS | STORAGE | ALL }

and _partition_bound_spec_ is:

IN ( _partition_bound_expr_ [, ...] ) |
FROM ( { _partition_bound_expr_ | MINVALUE | MAXVALUE } [, ...] )
  TO ( { _partition_bound_expr_ | MINVALUE | MAXVALUE } [, ...] ) |
WITH ( MODULUS _numeric_literal_, REMAINDER _numeric_literal_ )

_index_parameters_ in UNIQUE, PRIMARY KEY, and EXCLUDE constraints are:

[ INCLUDE ( _column_name_ [, ... ] ) ]
[ WITH ( _storage_parameter_ [= _value_] [, ... ] ) ]
[ USING INDEX TABLESPACE _tablespace_name_ ]

_exclude_element_ in an EXCLUDE constraint is:

{ _column_name_ | ( _expression_ ) } [ COLLATE _collation_ ] [ _opclass_ [ ( _opclass_parameter_ = _value_ [, ... ] ) ] ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ]

_referential_action_ in a FOREIGN KEY/REFERENCES constraint is:

{ NO ACTION | RESTRICT | CASCADE | SET NULL [ ( _column_name_ [, ... ] ) ] | SET DEFAULT [ ( _column_name_ [, ... ] ) ] }
```

--------------------------------

### GET pg_wait_events

Source: https://www.postgresql.org/docs/current/view-pg-wait-events.html

The view pg_wait_events provides description about the wait events occurring within the system.

```APIDOC
## GET pg_wait_events

### Description
The view pg_wait_events provides description about the wait events.

### Method
GET

### Endpoint
pg_wait_events

### Parameters

### Response
#### Success Response (200)
- **type** (text) - Wait event type
- **name** (text) - Wait event name
- **description** (text) - Wait event description

#### Response Example
[
  {
    "type": "LWLock",
    "name": "ProcArrayLock",
    "description": "Waiting to examine or change the proc array or get a snapshot."
  }
]
```

--------------------------------

### Demonstrate Two-Phase Commit with pg_recvlogical and psql

Source: https://www.postgresql.org/docs/current/logicaldecoding-example.html

This sequence of commands illustrates the lifecycle of a two-phase transaction, from slot creation and transaction preparation to commit or rollback, using both pg_recvlogical and psql.

```bash
$ pg_recvlogical -d postgres --slot=test --create-slot --enable-two-phase
```

```bash
$ pg_recvlogical -d postgres --slot=test --start -f -
```

```bash
$ psql -d postgres -c "BEGIN;INSERT INTO data(data) VALUES('5');PREPARE TRANSACTION 'test';"
```

```bash
$ fg
```

```bash
BEGIN 694
table public.data: INSERT: id[integer]:5 data[text]:'5'
PREPARE TRANSACTION 'test', txid 694
```

```bash
$ psql -d postgres -c "COMMIT PREPARED 'test';"
```

```bash
$ fg
```

```bash
COMMIT PREPARED 'test', txid 694
```

```bash
$ pg_recvlogical -d postgres --slot=test --drop-slot
```

--------------------------------

### GET pg_stat_ssl

Source: https://www.postgresql.org/docs/current/monitoring-stats.html

Shows statistics about SSL usage for each backend or WAL sender process connection.

```APIDOC
## GET pg_stat_ssl

### Description
The pg_stat_ssl view contains one row per backend or WAL sender process, showing statistics about SSL usage on the connection. It can be joined to pg_stat_activity or pg_stat_replication on the pid column.

### Method
GET

### Endpoint
pg_stat_ssl

### Response
#### Success Response (200)
- **pid** (integer) - Process ID of a backend or WAL sender process
- **ssl** (boolean) - True if SSL is used on this connection
- **version** (text) - Version of SSL in use, or NULL if not in use
- **cipher** (text) - Name of SSL cipher in use, or NULL if not in use
- **bits** (integer) - Number of bits in the encryption algorithm used, or NULL if not in use
- **client_dn** (text) - Distinguished Name (DN) field from the client certificate
- **client_serial** (numeric) - Serial number of the client certificate
- **issuer_dn** (text) - DN of the issuer of the client certificate
```

--------------------------------

### Get column name with PQfname

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Returns the name associated with a column number; do not free the result.

```c
char *PQfname(const PGresult *res,
              int column_number);
```

--------------------------------

### Get tsquery node count

Source: https://www.postgresql.org/docs/current/functions-textsearch.html

Returns the count of lexemes and operators combined within a tsquery.

```SQL
numnode('(fat & rat) | cat'::tsquery)
```

--------------------------------

### Pass PostgreSQL Server Parameters via Command Line

Source: https://www.postgresql.org/docs/current/config-setting.html

Configure PostgreSQL server startup parameters using the -c or --name=value syntax. These settings override postgresql.conf and ALTER SYSTEM but require server restart to change globally.

```Shell
postgres -c log_connections=all --log-destination='syslog'
```

--------------------------------

### Create and Execute Prepared SELECT Statement (PostgreSQL)

Source: https://www.postgresql.org/docs/current/sql-prepare.html

This example shows how to create a prepared statement for a SELECT query, where the data type of the second parameter is inferred from its usage context.

```sql
PREPARE usrrptplan (int) AS
    SELECT * FROM users u, logs l WHERE u.usrid=$1 AND u.usrid=l.usrid
    AND l.date = $2;
EXECUTE usrrptplan(1, current_date);
```

--------------------------------

### Get the upper bound of an array dimension

Source: https://www.postgresql.org/docs/current/functions-array.html

Returns the index of the last element in the specified dimension.

```sql
array_upper(ARRAY[1,8,3,7], 1)
```

--------------------------------

### GET /pg_trigger

Source: https://www.postgresql.org/docs/current/catalog-pg-trigger.html

Retrieve metadata for triggers defined on tables and views from the pg_trigger system catalog.

```APIDOC
## GET /pg_trigger

### Description
The catalog pg_trigger stores triggers on tables and views. It provides detailed information about trigger firing conditions, associated functions, and internal generation status.

### Method
GET

### Endpoint
/pg_trigger

### Response
#### Success Response (200)
- **oid** (oid) - Row identifier
- **tgrelid** (oid) - The table this trigger is on (references pg_class.oid)
- **tgparentid** (oid) - Parent trigger that this trigger is cloned from; zero if not a clone
- **tgname** (name) - Trigger name (unique among triggers of same table)
- **tgfoid** (oid) - The function to be called (references pg_proc.oid)
- **tgtype** (int2) - Bit mask identifying trigger firing conditions
- **tgenabled** (char) - Controls in which session_replication_role modes the trigger fires (O = origin/local, D = disabled, R = replica, A = always)
- **tgisinternal** (bool) - True if trigger is internally generated
- **tgconstrrelid** (oid) - The table referenced by a referential integrity constraint
- **tgconstrindid** (oid) - The index supporting a unique, primary key, referential integrity, or exclusion constraint
- **tgconstraint** (oid) - The pg_constraint entry associated with the trigger
- **tgdeferrable** (bool) - True if constraint trigger is deferrable
- **tginitdeferred** (bool) - True if constraint trigger is initially deferred
- **tgnargs** (int2) - Number of argument strings passed to trigger function
- **tgattr** (int2vector) - Column numbers, if trigger is column-specific; otherwise an empty array
- **tgargs** (bytea) - Argument strings to pass to trigger, each NULL-terminated
- **tgqual** (pg_node_tree) - Expression tree for the trigger's WHEN condition, or null if none
- **tgoldtable** (name) - REFERENCING clause name for OLD TABLE, or null if none
- **tgnewtable** (name) - REFERENCING clause name for NEW TABLE, or null if none

#### Response Example
{
  "oid": 16391,
  "tgrelid": 16384,
  "tgparentid": 0,
  "tgname": "example_trigger",
  "tgfoid": 16389,
  "tgtype": 21,
  "tgenabled": "O",
  "tgisinternal": false,
  "tgdeferrable": false,
  "tginitdeferred": false
}
```

--------------------------------

### GET /pg_transform

Source: https://www.postgresql.org/docs/current/catalog-pg-transform.html

Retrieve information about transforms used to adapt data types to procedural languages.

```APIDOC
## GET /pg_transform

### Description
The catalog pg_transform stores information about transforms, which are a mechanism to adapt data types to procedural languages.

### Method
GET

### Endpoint
/pg_transform

### Parameters
#### Table Columns
- **oid** (oid) - Required - Row identifier
- **trftype** (oid) - Required - OID of the data type this transform is for (references pg_type.oid)
- **trflang** (oid) - Required - OID of the language this transform is for (references pg_language.oid)
- **trffromsql** (regproc) - Required - The OID of the function to use when converting the data type for input to the procedural language (e.g., function parameters). Zero is stored if the default behavior should be used.
- **trftosql** (regproc) - Required - The OID of the function to use when converting output from the procedural language (e.g., return values) to the data type. Zero is stored if the default behavior should be used.

### Response
#### Success Response (200)
- **oid** (oid) - Row identifier
- **trftype** (oid) - Data type OID
- **trflang** (oid) - Language OID
- **trffromsql** (regproc) - Input conversion function OID
- **trftosql** (regproc) - Output conversion function OID
```

--------------------------------

### SPI Function Sample Session with SQL Operations

Source: https://www.postgresql.org/docs/current/spi-examples.html

Demonstrates the execq function behavior across multiple SQL operations including table creation, inserts, selects, and deletes. Shows how row counts are returned and illustrates data visibility rules within SPI execution.

```SQL
=> SELECT execq('CREATE TABLE a (x integer)', 0);
 execq
-------
     0
(1 row)

=> INSERT INTO a VALUES (execq('INSERT INTO a VALUES (0)', 0));
INSERT 0 1
=> SELECT execq('SELECT * FROM a', 0);
INFO:  EXECQ:  0    _-- inserted by execq_
INFO:  EXECQ:  1    _-- returned by execq and inserted by upper INSERT_

 execq
-------
     2
(1 row)

=> SELECT execq('INSERT INTO a SELECT x + 2 FROM a RETURNING *', 1);
INFO:  EXECQ:  2    _-- 0 + 2, then execution was stopped by count_
 execq
-------
     1
(1 row)

=> SELECT execq('SELECT * FROM a', 10);
INFO:  EXECQ:  0
INFO:  EXECQ:  1
INFO:  EXECQ:  2

 execq
-------
     3              _-- 10 is the max value only, 3 is the real number of rows_
(1 row)

=> SELECT execq('INSERT INTO a SELECT x + 10 FROM a', 1);
 execq
-------
     3              _-- all rows processed; count does not stop it, because nothing is returned_
(1 row)

=> SELECT * FROM a;
 x
----
  0
  1
  2
 10
 11
 12
(6 rows)

=> DELETE FROM a;
DELETE 6
=> INSERT INTO a VALUES (execq('SELECT * FROM a', 0) + 1);
INSERT 0 1
=> SELECT * FROM a;
 x
---
 1                  _-- 0 (no rows in a) + 1_
(1 row)

=> INSERT INTO a VALUES (execq('SELECT * FROM a', 0) + 1);
INFO:  EXECQ:  1
INSERT 0 1
=> SELECT * FROM a;
 x
---
 1
 2                  _-- 1 (there was one row in a) + 1_
(2 rows)

_-- This demonstrates the data changes visibility rule._
_-- execq is called twice and sees different numbers of rows each time:_

=> INSERT INTO a SELECT execq('SELECT * FROM a', 0) * x FROM a;
INFO:  EXECQ:  1    _-- results from first execq_
INFO:  EXECQ:  2
INFO:  EXECQ:  1    _-- results from second execq_
INFO:  EXECQ:  2
INFO:  EXECQ:  2
INSERT 0 2
=> SELECT * FROM a;
 x
---
 1
 2
 2                  _-- 2 rows * 1 (x in first row)_
 6                  _-- 3 rows (2 + 1 just inserted) * 2 (x in second row)_
(4 rows)
```

--------------------------------

### Create Multiple Single-Column B-tree Indexes and Analyze Query (PostgreSQL)

Source: https://www.postgresql.org/docs/current/bloom.html

This example creates separate B-tree indexes for each column in `tbloom` and then analyzes a query, demonstrating how the planner can use multiple indexes for better performance when leading columns are not constrained.

```sql
=# CREATE INDEX btreeidx1 ON tbloom (i1);
CREATE INDEX
=# CREATE INDEX btreeidx2 ON tbloom (i2);
CREATE INDEX
=# CREATE INDEX btreeidx3 ON tbloom (i3);
CREATE INDEX
=# CREATE INDEX btreeidx4 ON tbloom (i4);
CREATE INDEX
=# CREATE INDEX btreeidx5 ON tbloom (i5);
CREATE INDEX
=# CREATE INDEX btreeidx6 ON tbloom (i6);
CREATE INDEX
=# EXPLAIN ANALYZE SELECT * FROM tbloom WHERE i2 = 898732 AND i5 = 123451;
                                                        QUERY PLAN
-------------------------------------------------------------------u200b--------------------------------------------------------
 Bitmap Heap Scan on tbloom  (cost=9.29..13.30 rows=1 width=24) (actual time=0.032..0.033 rows=0.00 loops=1)
   Recheck Cond: ((i5 = 123451) AND (i2 = 898732))
   Buffers: shared read=6
   ->  BitmapAnd  (cost=9.29..9.29 rows=1 width=0) (actual time=0.047..0.047 rows=0.00 loops=1)
         Buffers: shared hit=6
         ->  Bitmap Index Scan on btreeidx5  (cost=0.00..4.52 rows=11 width=0) (actual time=0.026..0.026 rows=7.00 loops=1)
               Index Cond: (i5 = 123451)
               Index Searches: 1
               Buffers: shared hit=3
```

--------------------------------

### Remove a specific materialized view

Source: https://www.postgresql.org/docs/current/sql-dropmaterializedview.html

This example demonstrates how to delete a materialized view named order_summary.

```sql
DROP MATERIALIZED VIEW order_summary;

```

--------------------------------

### Drop a specific access method

Source: https://www.postgresql.org/docs/current/sql-drop-access-method.html

This example demonstrates how to drop an access method named `heptree`.

```sql
DROP ACCESS METHOD heptree;
```

--------------------------------

### Configure auto_explain in postgresql.conf

Source: https://www.postgresql.org/docs/current/auto-explain.html

Set up auto_explain module with session preloading and minimum duration threshold. Place these settings in postgresql.conf to enable automatic query plan logging for queries exceeding 3 seconds.

```ini
# postgresql.conf
session_preload_libraries = 'auto_explain'

auto_explain.log_min_duration = '3s'
```

--------------------------------

### Create Prepared Statement with PQprepare

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Submits a request to create a prepared statement for later execution. Use stmtName "" for an unnamed statement and paramTypes to specify OIDs for parameters.

```c
PGresult *PQprepare(PGconn *conn,
                    const char *stmtName,
                    const char *query,
                    int nParams,
                    const Oid *paramTypes);

```

--------------------------------

### JSON_VALUE Examples

Source: https://www.postgresql.org/docs/current/functions-json.html

Common usage patterns for JSON_VALUE including type casting and error handling.

```APIDOC
## EXAMPLES

### Description
Demonstration of type conversion, date parsing, and error handling using the DEFAULT clause.

### Method
SQL QUERY

### Endpoint
JSON_VALUE Examples

### Request Example
```sql
-- Example 1: Returning float
JSON_VALUE(jsonb '"123.45"', '$' RETURNING float);

-- Example 2: Parsing datetime
JSON_VALUE(jsonb '"03:04 2015-02-01"', '$.datetime("HH24:MI YYYY-MM-DD")' RETURNING date);

-- Example 3: Error handling with default
JSON_VALUE(jsonb '[1,2]', 'strict $[*]' DEFAULT 9 ON ERROR);
```

### Response
#### Success Response
- **Example 1 Result**: 123.45
- **Example 2 Result**: 2015-02-01
- **Example 3 Result**: 9
```

--------------------------------

### Insert initial data on publisher

Source: https://www.postgresql.org/docs/current/logical-replication-subscription.html

Insert sample data into the three tables on the publisher side before setting up replication.

```SQL
/* pub # */ INSERT INTO t1 VALUES (1, 'one'), (2, 'two'), (3, 'three');
/* pub # */ INSERT INTO t2 VALUES (1, 'A'), (2, 'B'), (3, 'C');
/* pub # */ INSERT INTO t3 VALUES (1, 'i'), (2, 'ii'), (3, 'iii');
```

--------------------------------

### pg_prewarm Configuration in postgresql.conf

Source: https://www.postgresql.org/docs/current/pgprewarm.html

Configuration example showing how to enable pg_prewarm module with autoprewarm settings. Must be set in postgresql.conf; autoprewarm_interval controls how often autoprewarm.blocks is updated (0 disables regular updates).

```INI
# postgresql.conf
shared_preload_libraries = 'pg_prewarm'

pg_prewarm.autoprewarm = true
pg_prewarm.autoprewarm_interval = 300s
```

--------------------------------

### Create postgres_fdw Extension in PostgreSQL

Source: https://www.postgresql.org/docs/current/postgres-fdw.html

Install the `postgres_fdw` extension to enable foreign data wrapper capabilities.

```sql
CREATE EXTENSION postgres_fdw;

```

--------------------------------

### Window Frame Boundary Options

Source: https://www.postgresql.org/docs/current/sql-expressions.html

Valid expressions for defining the start and end boundaries of a window frame.

```sql
UNBOUNDED PRECEDING
_offset_ PRECEDING
CURRENT ROW
_offset_ FOLLOWING
UNBOUNDED FOLLOWING

```

--------------------------------

### LISTEN command synopsis

Source: https://www.postgresql.org/docs/current/sql-listen.htm

The basic syntax for registering the current session as a listener on a notification channel.

```sql
LISTEN _channel_
```

--------------------------------

### pg_ctl - Control PostgreSQL Server

Source: https://www.postgresql.org/docs/current/reference-server.html

A utility for initializing, starting, stopping, or controlling the PostgreSQL server process.

```APIDOC
## EXEC pg_ctl

### Description
Initialize, start, stop, or control a PostgreSQL server.

### Method
CLI

### Endpoint
pg_ctl
```

--------------------------------

### PQconnectStartParams - Initiate Nonblocking Connection with Parameters

Source: https://www.postgresql.org/docs/current/libpq-connect.html

Initiates a nonblocking connection to a PostgreSQL database server using separate keyword and value arrays. Similar to PQconnectStart but accepts parameters as arrays instead of a connection string, providing more structured parameter passing.

```APIDOC
## PQconnectStartParams

### Description
Initiates a nonblocking connection to a PostgreSQL database server using keyword and value parameter arrays.

### Function Signature
```c
PGconn *PQconnectStartParams(const char * const *keywords,
                             const char * const *values,
                             int expand_dbname);
```

### Parameters
#### Function Parameters
- **keywords** (const char * const *) - Required - Array of parameter keywords (e.g., "host", "port", "dbname")
- **values** (const char * const *) - Required - Array of parameter values corresponding to keywords
- **expand_dbname** (int) - Required - Controls whether the dbname parameter is expanded; see PQconnectdbParams documentation for details

### Return Value
- **PGconn*** - A pointer to a new PGconn structure, or NULL if memory allocation fails. A non-null return does not indicate a successful connection; use PQstatus() or PQconnectPoll() to check connection status.

### Notes
- Does not block on remote I/O operations
- Must be followed by PQconnectPoll() calls to complete the connection sequence
- Provides structured parameter passing compared to PQconnectStart's connection string approach
```

--------------------------------

### Variable conflict resolution options

Source: https://www.postgresql.org/docs/current/plpgsql-implementation.html

Directives used at the start of a function to override the global plpgsql.variable_conflict setting.

```plpgsql
#variable_conflict error
#variable_conflict use_variable
#variable_conflict use_column

```

--------------------------------

### Dynamic PREPARE in ECPG with C

Source: https://www.postgresql.org/docs/current/ecpg-sql-prepare.html

This C code snippet demonstrates how to dynamically prepare an SQL statement using a host variable and the EXEC SQL PREPARE command in an ECPG program. The prepared statement 'foo' can then be executed.

```C
char *stmt = "SELECT * FROM test1 WHERE a = ? AND b = ?";

EXEC SQL ALLOCATE DESCRIPTOR outdesc;
EXEC SQL PREPARE foo FROM :stmt;

EXEC SQL EXECUTE foo USING SQL DESCRIPTOR indesc INTO SQL DESCRIPTOR outdesc;
```

--------------------------------

### PQuntrace - Disable client/server tracing in libpq

Source: https://www.postgresql.org/docs/current/libpq-control.html

Disables tracing previously started by PQtrace on the given connection.

```C
void PQuntrace(PGconn *conn);
```

--------------------------------

### Create an Empty Database from template0

Source: https://www.postgresql.org/docs/current/app-pgrestore.html

Use this SQL command to create a new database that is truly empty, without any local additions that might be present in 'template1'. This helps avoid errors due to duplicate definitions during a restore.

```sql
CREATE DATABASE foo WITH TEMPLATE template0;
```

--------------------------------

### Extract substring by index in PostgreSQL

Source: https://www.postgresql.org/docs/current/functions-string.html

Extracts a substring starting at a specific character position for an optional length.

```sql
substr('alphabet', 3)
```

```sql
substr('alphabet', 3, 2)
```

--------------------------------

### REPLICATION / SHOW

Source: https://www.postgresql.org/docs/current/protocol-replication.html

Requests the server to send the current setting of a run-time parameter, similar to the standard SQL SHOW command.

```APIDOC
## REPLICATION SHOW

### Description
Requests the server to send the current setting of a run-time parameter.

### Method
REPLICATION COMMAND

### Endpoint
SHOW [name]

### Parameters
#### Path Parameters
- **name** (string) - Required - The name of a run-time parameter.

### Request Example
SHOW max_wal_senders;
```

--------------------------------

### SELECT trim

Source: https://www.postgresql.org/docs/current/functions-string.html

Removes the longest string containing only specified characters from the start, end, or both ends of a string.

```APIDOC
## SELECT trim

### Description
Removes specified characters (space by default) from the start, end, or both ends of a string.

### Method
SQL FUNCTION

### Endpoint
trim([LEADING | TRAILING | BOTH] [characters text] FROM string text)

### Parameters
#### Path Parameters
- **direction** (keyword) - Optional - LEADING, TRAILING, or BOTH (default).
- **characters** (text) - Optional - Characters to remove (default is space).
- **string** (text) - Required - The target string.

### Request Example
SELECT trim(both 'xyz' from 'yxTomxx');

### Response
#### Success Response (200)
- **result** (text) - The trimmed string.

#### Response Example
"Tom"
```

--------------------------------

### Extract substring from bytea in SQL

Source: https://www.postgresql.org/docs/current/functions-binarystring.html

Extracts a substring of _bytes_ starting at _start_ and stopping after _count_ bytes.

```SQL
substring('\x1234567890'::bytea from 3 for 2)
```

--------------------------------

### ROLLBACK PREPARED - Example Usage

Source: https://www.postgresql.org/docs/current/sql-rollback-prepared.html

Demonstrates rolling back a specific prepared transaction identified by 'foobar'. This command executes immediately and cannot be used within a transaction block.

```sql
ROLLBACK PREPARED 'foobar';
```

--------------------------------

### Overlay substring in bytea in SQL

Source: https://www.postgresql.org/docs/current/functions-binarystring.html

Replaces a substring of _bytes_ with _newsubstring_ starting at _start_ for _count_ bytes.

```SQL
overlay('\x1234567890'::bytea placing '\002\003'::bytea from 2 for 3)
```

--------------------------------

### GET pg_stat_gssapi

Source: https://www.postgresql.org/docs/current/monitoring-stats.html

Provides information about GSSAPI usage, including authentication and encryption status, for each backend connection.

```APIDOC
## GET pg_stat_gssapi

### Description
The pg_stat_gssapi view contains one row per backend, showing information about GSSAPI usage on the connection. It can be joined to pg_stat_activity or pg_stat_replication on the pid column.

### Method
GET

### Endpoint
pg_stat_gssapi

### Response
#### Success Response (200)
- **pid** (integer) - Process ID of a backend
- **gss_authenticated** (boolean) - True if GSSAPI authentication was used for this connection
- **principal** (text) - Principal used to authenticate this connection
- **encrypted** (boolean) - True if GSSAPI encryption is in use on this connection
- **credentials_delegated** (boolean) - True if GSSAPI credentials were delegated on this connection
```

--------------------------------

### SQL POSIX Regex Basic Pattern Examples

Source: https://www.postgresql.org/docs/current/functions-matching.html

Illustrates fundamental POSIX regular expression patterns and their matching behavior using the '~' operator in SQL.

```SQL
'abcd' ~ 'bc'
```

```SQL
'abcd' ~ 'a.c'
```

```SQL
'abcd' ~ 'a.*d'
```

```SQL
'abcd' ~ '(b|x)'
```

```SQL
'abcd' ~ '^a'
```

```SQL
'abcd' ~ '^(b|c)'
```

--------------------------------

### GET pg_stat_subscription_stats

Source: https://www.postgresql.org/docs/current/monitoring-stats.html

Provides statistics about subscription errors and conflicts. It contains one row per subscription.

```APIDOC
## GET pg_stat_subscription_stats

### Description
The pg_stat_subscription_stats view contains one row per subscription, tracking errors and conflicts encountered during the application of changes and initial synchronization.

### Method
GET

### Endpoint
pg_stat_subscription_stats

### Response
#### Success Response (200)
- **subid** (oid) - OID of the subscription
- **subname** (name) - Name of the subscription
- **apply_error_count** (bigint) - Number of times an error occurred while applying changes
- **sync_error_count** (bigint) - Number of times an error occurred during the initial table synchronization
- **confl_insert_exists** (bigint) - Number of times a row insertion violated a NOT DEFERRABLE unique constraint
- **confl_update_origin_differs** (bigint) - Number of times an update was applied to a row previously modified by another source
- **confl_update_exists** (bigint) - Number of times an updated row value violated a NOT DEFERRABLE unique constraint
- **confl_update_missing** (bigint) - Number of times the tuple to be updated was not found
- **confl_delete_origin_differs** (bigint) - Number of times a delete operation was applied to a row previously modified by another source
- **confl_delete_missing** (bigint) - Number of times the tuple to be deleted was not found
- **confl_multiple_unique_conflicts** (bigint) - Number of times a row operation violated multiple NOT DEFERRABLE unique constraints
- **stats_reset** (timestamp with time zone) - Time at which these statistics were last reset
```

--------------------------------

### EXECUTE Comparison with Direct PL/pgSQL Execution

Source: https://www.postgresql.org/docs/current/plpgsql-statements.html

Explains the differences between EXECUTE with parameters and direct PL/pgSQL command execution. Highlights plan caching behavior and when to use EXECUTE for optimal performance.

```APIDOC
## EXECUTE vs Direct PL/pgSQL Execution

### Description
An EXECUTE statement with a simple constant command string and USING parameters is functionally equivalent to writing the command directly in PL/pgSQL. However, there are important differences in plan caching and optimization behavior.

### Functional Equivalence

#### Direct PL/pgSQL Execution
```sql
SELECT count(*) INTO c FROM mytable 
WHERE inserted_by = checked_user AND inserted <= checked_date;
```

#### EXECUTE with Parameters
```sql
EXECUTE 'SELECT count(*) FROM mytable WHERE inserted_by = $1 AND inserted <= $2'
   INTO c
   USING checked_user, checked_date;
```

Both produce the same result, but differ in plan caching behavior.

### Plan Caching Differences

#### Direct PL/pgSQL Execution
- PL/pgSQL may create a generic plan and cache it for re-use
- The cached plan is used for all subsequent executions
- Generic plans may not be optimal for all parameter values

#### EXECUTE Statement
- No plan caching occurs
- Command is re-planned on each execution
- Generated plan is specific to the current parameter values
- Ensures optimal plan selection based on actual parameter values

### Performance Considerations

#### When to Use EXECUTE
- When the best plan depends strongly on parameter values
- To positively ensure a generic plan is not selected
- When parameter value distributions vary significantly
- When query selectivity depends heavily on parameter values

#### When Direct Execution is Sufficient
- When query plans are relatively stable across parameter values
- When plan caching provides performance benefits
- For simple queries where plan variation is minimal
```

--------------------------------

### Get column internal size with PQfsize

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Returns the size in bytes of the server's internal representation.

```c
int PQfsize(const PGresult *res,
            int column_number);
```

--------------------------------

### Get column type modifier with PQfmod

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Returns type-specific modifiers like precision or size limits.

```c
int PQfmod(const PGresult *res,
           int column_number);
```

--------------------------------

### VACUUM with VERBOSE and ANALYZE options

Source: https://www.postgresql.org/docs/current/sql-vacuum.htm

Clean a single table, analyze it for the optimizer, and print a detailed vacuum activity report. Requires MAINTAIN privilege on the table or database owner status.

```SQL
VACUUM (VERBOSE, ANALYZE) onek;
```

--------------------------------

### Run pgbench with aggregated logging and detailed failure reporting

Source: https://www.postgresql.org/docs/current/pgbench.html

Use the --aggregate-interval option to generate summarized logs. This example includes rate limiting, latency limits, and detailed failure statistics for serialization and deadlock errors.

```shell
**pgbench --aggregate-interval=10 --time=20 --client=10 --log --rate=1000 --latency-limit=10 --failures-detailed --max-tries=10 test**

1650260552 5178 26171317 177284491527 1136 44462 2647617 7321113867 0 9866 64 7564 28340 4148 0
1650260562 4808 25573984 220121792172 1171 62083 3037380 9666800914 0 9998 598 7392 26621 4527 0

```

--------------------------------

### Get column format with PQfformat

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Returns the format code (0 for text, 1 for binary) of a column.

```c
int PQfformat(const PGresult *res,
              int column_number);
```

--------------------------------

### GET information_schema.foreign_server_options

Source: https://www.postgresql.org/docs/current/infoschema-foreign-server-options.html

Retrieves all options defined for foreign servers in the current database that the current user has access to.

```APIDOC
## GET information_schema.foreign_server_options

### Description
The view foreign_server_options contains all the options defined for foreign servers in the current database. Only those foreign servers are shown that the current user has access to (by way of being the owner or having some privilege).

### Method
GET

### Endpoint
information_schema.foreign_server_options

### Response
#### Success Response (200)
- **foreign_server_catalog** (sql_identifier) - Name of the database that the foreign server is defined in (always the current database)
- **foreign_server_name** (sql_identifier) - Name of the foreign server
- **option_name** (sql_identifier) - Name of an option
- **option_value** (character_data) - Value of the option

#### Response Example
{
  "foreign_server_catalog": "postgres",
  "foreign_server_name": "remote_server",
  "option_name": "host",
  "option_value": "10.0.0.1"
}
```

--------------------------------

### CREATE ROLE Syntax Synopsis

Source: https://www.postgresql.org/docs/current/sql-createrole.html

General syntax for creating a role with various options for privileges, connection limits, and authentication.

```sql
CREATE ROLE _name_ [ [ WITH ] _option_ [ ... ] ]

where _option_ can be:

      SUPERUSER | NOSUPERUSER
    | CREATEDB | NOCREATEDB
    | CREATEROLE | NOCREATEROLE
    | INHERIT | NOINHERIT
    | LOGIN | NOLOGIN
    | REPLICATION | NOREPLICATION
    | BYPASSRLS | NOBYPASSRLS
    | CONNECTION LIMIT _connlimit_
    | [ ENCRYPTED ] PASSWORD '_password_' | PASSWORD NULL
    | VALID UNTIL '_timestamp_'
    | IN ROLE _role_name_ [, ...]
    | ROLE _role_name_ [, ...]
    | ADMIN _role_name_ [, ...]
    | SYSID _uid_
```

--------------------------------

### Initialize PostgreSQL with mixed locale settings

Source: https://www.postgresql.org/docs/current/locale.html

This `initdb` command demonstrates how to set a primary locale (French Canadian) while overriding a specific subcategory (monetary formatting) to use rules from a different locale (U.S. English).

```shell
initdb --locale=fr_CA --lc-monetary=en_US
```

--------------------------------

### Get current date using PGTYPESdate_today

Source: https://www.postgresql.org/docs/current/ecpg-pgtypes.html

Sets the provided date variable to the current system date.

```c
void PGTYPESdate_today(date *d);

```

--------------------------------

### GET GetUserMapping / GetForeignTable

Source: https://www.postgresql.org/docs/current/fdw-helpers.html

Functions to retrieve user mapping and foreign table metadata based on OIDs.

```APIDOC
## GET GetUserMapping

### Description
Returns a UserMapping object for the user mapping of the given role on the given server. Falls back to PUBLIC mapping if specific user mapping is missing.

### Method
GET

### Endpoint
GetUserMapping(Oid userid, Oid serverid)

### Parameters
#### Path Parameters
- **userid** (Oid) - Required - The OID of the user role.
- **serverid** (Oid) - Required - The OID of the foreign server.

### Response
#### Success Response (200)
- **UserMapping*** (struct) - Pointer to the user mapping properties.

---

## GET GetForeignTable

### Description
Returns a ForeignTable object for the foreign table with the given OID.

### Method
GET

### Endpoint
GetForeignTable(Oid relid)

### Parameters
#### Path Parameters
- **relid** (Oid) - Required - The OID of the foreign table relation.

### Response
#### Success Response (200)
- **ForeignTable*** (struct) - Pointer to the foreign table properties.
```

--------------------------------

### Call `anycompatible` Function with Mixed Types

Source: https://www.postgresql.org/docs/current/plpgsql-declarations.html

Example call to a function using `anycompatible` types, demonstrating automatic type promotion for integer and numeric inputs.

```sql
SELECT add_three_values(1, 2, 4.7);
```

--------------------------------

### Get Foreign Server by OID

Source: https://www.postgresql.org/docs/current/fdw-helpers.html

Retrieve a ForeignServer object by OID. Raises an error if the server does not exist.

```C
ForeignServer *
GetForeignServer(Oid serverid);
```

--------------------------------

### GET /pg_catalog/pg_default_acl

Source: https://www.postgresql.org/docs/current/catalog-pg-default-acl.html

Retrieves the initial privileges assigned to newly created objects for specific roles and namespaces.

```APIDOC
## GET /pg_catalog/pg_default_acl\n\n### Description\nThe catalog pg_default_acl stores initial privileges to be assigned to newly created objects. It is consulted during object creation to determine default permissions.\n\n### Method\nGET\n\n### Endpoint\n/pg_catalog/pg_default_acl\n\n### Parameters\n#### Table Columns\n- **oid** (oid) - Required - Row identifier\n- **defaclrole** (oid) - Required - The OID of the role associated with this entry (references pg_authid.oid)\n- **defaclnamespace** (oid) - Required - The OID of the namespace associated with this entry, or zero if none (references pg_namespace.oid)\n- **defaclobjtype** (char) - Required - Type of object: r = relation (table, view), S = sequence, f = function, T = type, n = schema, L = large object\n- **defaclacl** (aclitem[]) - Required - Access privileges that this type of object should have on creation\n\n### Request Example\nSELECT * FROM pg_catalog.pg_default_acl;\n\n### Response\n#### Success Response (200)\n- **oid** (oid) - Row identifier\n- **defaclrole** (oid) - Role OID associated with the entry\n- **defaclnamespace** (oid) - Namespace OID or zero for global entries\n- **defaclobjtype** (char) - Character code representing the object type\n- **defaclacl** (aclitem[]) - Array of access privileges\n\n#### Response Example\n{\n  "oid": 16384,\n  "defaclrole": 10,\n  "defaclnamespace": 0,\n  "defaclobjtype": "r",\n  "defaclacl": ["=r/postgres"]\n}
```

--------------------------------

### ExplainCustomScan Callback

Source: https://www.postgresql.org/docs/current/custom-scan-execution.html

Output additional information for EXPLAIN of a custom-scan plan node.

```c
void (*ExplainCustomScan) (CustomScanState *node,
                           List *ancestors,
                           ExplainState *es);
```

--------------------------------

### Case-Insensitive Unquoted Identifiers Example

Source: https://www.postgresql.org/docs/current/sql-syntax-lexical.html

Demonstrates that unquoted identifiers and key words are treated as case-insensitive in PostgreSQL.

```SQL
uPDaTE my_TabLE SeT a = 5;
```

--------------------------------

### Recreate database from dump

Source: https://www.postgresql.org/docs/current/app-pgrestore.html

Drops the existing database and uses the -C flag to recreate it from the archive. The -d switch connects to an existing database to issue the creation command.

```shell
$ **dropdb mydb**
$ **pg_restore -C -d postgres db.dump**
```

--------------------------------

### Drop transform for hstore and plpython3u

Source: https://www.postgresql.org/docs/current/sql-droptransform.html

Specific example removing the transform for the hstore type and plpython3u language.

```sql
DROP TRANSFORM FOR hstore LANGUAGE plpython3u;

```

--------------------------------

### CREATE SUBSCRIPTION Syntax

Source: https://www.postgresql.org/docs/current/sql-createsubscription.html

This snippet shows the basic syntax for creating a new logical replication subscription, including connection information, publication names, and optional parameters.

```sql
CREATE SUBSCRIPTION _subscription_name_
    CONNECTION '_conninfo_'
    PUBLICATION _publication_name_ [, ...]
    [ WITH ( _subscription_parameter_ [= _value_] [, ... ] ) ]
```

--------------------------------

### Drop a specific trigger from a table

Source: https://www.postgresql.org/docs/current/sql-droptrigger.htm

Example of destroying a trigger named if_dist_exists associated with the films table.

```sql
DROP TRIGGER if_dist_exists ON films;
```

--------------------------------

### Basic DELETE operations

Source: https://www.postgresql.org/docs/current/sql-delete.htm

Examples of deleting specific rows based on a condition or clearing an entire table.

```sql
DELETE FROM films WHERE kind <> 'Musical';

```

```sql
DELETE FROM films;

```

--------------------------------

### \? Command

Source: https://www.postgresql.org/docs/current/app-psql.htm

Shows help information. The optional _topic_ parameter selects which part of psql is explained: commands, options, or variables.

```psql
\? [ _topic_]
```

--------------------------------

### Startup Callback

Source: https://www.postgresql.org/docs/current/oauth-validator-callbacks.html

The startup_cb callback is executed immediately after loading the OAuth validator module. It can be used to initialize local state and perform additional setup. Validator modules can store state data in state->private_data for later use.

```APIDOC
## Startup Callback

### Description
Executed directly after loading the OAuth validator module. Used for initialization and setting up local state.

### Callback Signature
```c
typedef void (*ValidatorStartupCB) (ValidatorModuleState *state);
```

### Parameters
#### Input Parameters
- **state** (ValidatorModuleState*) - Required - Module state structure that can store private data via state->private_data

### Usage
The validator module can use this callback to:
- Initialize internal data structures
- Set up resources needed for validation
- Store initialization state in state->private_data for use in subsequent callbacks
```

--------------------------------

### Rename a PostgreSQL Tablespace

Source: https://www.postgresql.org/docs/current/sql-altertablespace.html

Example demonstrating how to rename an existing tablespace using the `ALTER TABLESPACE` command.

```sql
ALTER TABLESPACE index_space RENAME TO fast_raid;
```

--------------------------------

### libpq Event Management with Private Data

Source: https://www.postgresql.org/docs/current/libpq-events.html

Complete example of registering an event processor with libpq to manage private data (instanceData) across connection and result lifecycles. Demonstrates event registration, data association, result copying with events, and proper cleanup.

```C
/* required header for libpq events (note: includes libpq-fe.h) */
#include <libpq-events.h>

/* The instanceData */
typedef struct
{
    int n;
    char *str;
} mydata;

/* PGEventProc */
static int myEventProc(PGEventId evtId, void *evtInfo, void *passThrough);

int
main(void)
{
    mydata *data;
    PGresult *res;
    PGconn *conn =
        PQconnectdb("dbname=postgres options=-csearch_path=");

    if (PQstatus(conn) != CONNECTION_OK)
    {
        /* PQerrorMessage's result includes a trailing newline */
        fprintf(stderr, "%s", PQerrorMessage(conn));
        PQfinish(conn);
        return 1;
    }

    /* called once on any connection that should receive events.
     * Sends a PGEVT_REGISTER to myEventProc.
     */
    if (!PQregisterEventProc(conn, myEventProc, "mydata_proc", NULL))
    {
        fprintf(stderr, "Cannot register PGEventProc\n");
        PQfinish(conn);
        return 1;
    }

    /* conn instanceData is available */
    data = PQinstanceData(conn, myEventProc);

    /* Sends a PGEVT_RESULTCREATE to myEventProc */
    res = PQexec(conn, "SELECT 1 + 1");

    /* result instanceData is available */
    data = PQresultInstanceData(res, myEventProc);

    /* If PG_COPYRES_EVENTS is used, sends a PGEVT_RESULTCOPY to myEventProc */
    res_copy = PQcopyResult(res, PG_COPYRES_TUPLES | PG_COPYRES_EVENTS);

    /* result instanceData is available if PG_COPYRES_EVENTS was
     * used during the PQcopyResult call.
     */
    data = PQresultInstanceData(res_copy, myEventProc);

    /* Both clears send a PGEVT_RESULTDESTROY to myEventProc */
    PQclear(res);
    PQclear(res_copy);

    /* Sends a PGEVT_CONNDESTROY to myEventProc */
    PQfinish(conn);

    return 0;
}

static int
myEventProc(PGEventId evtId, void *evtInfo, void *passThrough)
{
    switch (evtId)
    {
        case PGEVT_REGISTER:
        {
            PGEventRegister *e = (PGEventRegister *)evtInfo;
            mydata *data = get_mydata(e->conn);

            /* associate app specific data with connection */
            PQsetInstanceData(e->conn, myEventProc, data);
            break;
        }

        case PGEVT_CONNRESET:
        {
            PGEventConnReset *e = (PGEventConnReset *)evtInfo;
            mydata *data = PQinstanceData(e->conn, myEventProc);

            if (data)
              memset(data, 0, sizeof(mydata));
            break;
        }

        case PGEVT_CONNDESTROY:
        {
            PGEventConnDestroy *e = (PGEventConnDestroy *)evtInfo;
            mydata *data = PQinstanceData(e->conn, myEventProc);

            /* free instance data because the conn is being destroyed */
            if (data)
              free_mydata(data);
            break;
        }

        case PGEVT_RESULTCREATE:
        {
            PGEventResultCreate *e = (PGEventResultCreate *)evtInfo;
            mydata *conn_data = PQinstanceData(e->conn, myEventProc);
            mydata *res_data = dup_mydata(conn_data);

            /* associate app specific data with result (copy it from conn) */
            PQresultSetInstanceData(e->result, myEventProc, res_data);
            break;
        }

        case PGEVT_RESULTCOPY:
        {
            PGEventResultCopy *e = (PGEventResultCopy *)evtInfo;
            mydata *src_data = PQresultInstanceData(e->src, myEventProc);
            mydata *dest_data = dup_mydata(src_data);

            /* associate app specific data with result (copy it from a result) */
            PQresultSetInstanceData(e->dest, myEventProc, dest_data);
            break;
        }

        case PGEVT_RESULTDESTROY:
        {
            PGEventResultDestroy *e = (PGEventResultDestroy *)evtInfo;
            mydata *data = PQresultInstanceData(e->result, myEventProc);

            /* free instance data because the result is being destroyed */
            if (data)
              free_mydata(data);
            break;
        }

        /* unknown event ID, just return true. */
        default:
            break;
    }

    return true; /* event processing succeeded */
}
```

--------------------------------

### Change Owner of a PostgreSQL Conversion

Source: https://www.postgresql.org/docs/current/sql-alterconversion.html

Example showing how to change the owner of the 'iso_8859_1_to_utf8' conversion to the user 'joe'.

```SQL
ALTER CONVERSION iso_8859_1_to_utf8 OWNER TO joe;
```

--------------------------------

### SRF_PERCALL_SETUP() Macro

Source: https://www.postgresql.org/docs/current/xfunc-c.html

Sets up the `FuncCallContext` for use in the current call of a Set-Returning Function (SRF). This macro should be called on every invocation, including the first.

```APIDOC
## SRF_PERCALL_SETUP()

### Description
This macro must be called on every invocation of a ValuePerCall mode Set-Returning Function (SRF), after `SRF_FIRSTCALL_INIT()` (if it's the first call). It prepares the `FuncCallContext` for the current call, making its fields accessible.

### Method
Macro

### Endpoint
N/A (C-language macro)

### Parameters
N/A

### Request Example (Conceptual - C usage)
```c
SRF_PERCALL_SETUP();
// Access funcctx fields
```

### Response
N/A (Prepares context, no direct return value)
```

--------------------------------

### SQL Table Aliases for Self-Join

Source: https://www.postgresql.org/docs/current/queries-table-expressions.html

Example of using table aliases when joining a table to itself, which is a necessary application.

```SQL
SELECT * FROM people AS mother JOIN people AS child ON mother.id = child.mother_id;
```

--------------------------------

### Open a cursor using an input SQLDA

Source: https://www.postgresql.org/docs/current/ecpg-descriptors.html

Use `EXEC SQL OPEN` with the `USING DESCRIPTOR` clause to pass the prepared SQLDA as input parameters to a cursor.

```C
EXEC SQL OPEN cur1 USING DESCRIPTOR sqlda2;
```

--------------------------------

### Iterating Through Array Elements in PL/pgSQL

Source: https://www.postgresql.org/docs/current/plpgsql-control-structures.html

Example function that calculates the sum of an integer array by iterating through each element.

```sql
CREATE FUNCTION sum(int[]) RETURNS int8 AS $$
DECLARE
  s int8 := 0;
  x int;
BEGIN
  FOREACH x IN ARRAY $1
  LOOP
    s := s + x;
  END LOOP;
  RETURN s;
END;
$$ LANGUAGE plpgsql;
```

--------------------------------

### Start PostgreSQL server manually using postgres

Source: https://www.postgresql.org/docs/current/server-start.html

The -D option specifies the data directory location. Background execution requires manual redirection of stdout and stderr to a log file.

```shell
$ **postgres -D /usr/local/pgsql/data**

```

```shell
$ **postgres -D /usr/local/pgsql/data >logfile 2>&1 &**

```

--------------------------------

### Cube Intersection Function Basic Example

Source: https://www.postgresql.org/docs/current/cube.html

Illustrates the `cube_inter` function to find the intersection of two cubes.

```SQL
cube_inter('(1,2)', '(3,4)')
```

--------------------------------

### Using Bit String Types in PostgreSQL

Source: https://www.postgresql.org/docs/current/datatype-bit.html

This example demonstrates how to create a table with `BIT` and `BIT VARYING` columns, insert values, and observe length constraints and explicit casting behavior.

```SQL
CREATE TABLE test (a BIT(3), b BIT VARYING(5));
INSERT INTO test VALUES (B'101', B'00');
INSERT INTO test VALUES (B'10', B'101');

ERROR:  bit string length 2 does not match type bit(3)

INSERT INTO test VALUES (B'10'::bit(3), B'101');
SELECT * FROM test;
```

--------------------------------

### Start Generic WAL Record Construction in C

Source: https://www.postgresql.org/docs/current/generic-wal.html

Initiates the construction of a generic WAL record for a specified relation. This is the first step in logging data updates using the generic WAL facility.

```C
state = GenericXLogStart(relation)
```

--------------------------------

### Identity Column Data Example

Source: https://www.postgresql.org/docs/current/ddl-identity-columns.html

Illustrates the resulting data in a table after inserting values into an identity column.

```sql
 id | name | address
----+------+---------
  1 | A    | foo
  2 | B    | bar
```

--------------------------------

### Run PostgreSQL Regression Tests

Source: https://www.postgresql.org/docs/current/install-make.html

Execute this command to run the regression tests and verify the newly built server's functionality. This should be done as an unprivileged user.

```make
make check
```

--------------------------------

### Check Connection Status with dblink_is_busy

Source: https://www.postgresql.org/docs/current/contrib-dblink-is-busy.html

Example of how to check if a specific connection is currently busy with an asynchronous query.

```sql
SELECT dblink_is_busy('dtest1');

```

--------------------------------

### Basic JSON_TABLE query with WITH WRAPPER

Source: https://www.postgresql.org/docs/current/functions-json.html

Demonstrates mapping JSON keys to columns and using WITH WRAPPER to handle multiple matches as arrays.

```sql
SELECT jt.* FROM
 my_films,
 JSON_TABLE (js, '$.favorites[*]' COLUMNS (
   id FOR ORDINALITY,
   kind text PATH '$.kind',
   title text PATH '$.films[*].title' WITH WRAPPER,
   director text PATH '$.films[*].director' WITH WRAPPER)) AS jt;
```

```text
 id |   kind   |             title              |             director
----+----------+--------------------------------+----------------------------------
  1 | comedy   | ["Bananas", "The Dinner Game"] | ["Woody Allen", "Francis Veber"]
  2 | horror   | ["Psycho"]                     | ["Alfred Hitchcock"]
  3 | thriller | ["Vertigo"]                    | ["Alfred Hitchcock"]
  4 | drama    | ["Yojimbo"]                    | ["Akira Kurosawa"]
(4 rows)
```

--------------------------------

### Two-dimensional integer array constant

Source: https://www.postgresql.org/docs/current/arrays.htm

An example of a 3-by-3 multidimensional array literal consisting of three subarrays.

```sql
'{{1,2,3},{4,5,6},{7,8,9}}'
```

--------------------------------

### EXPLAIN ANALYZE without JIT in PostgreSQL

Source: https://www.postgresql.org/docs/current/jit-decision.html

Use `EXPLAIN ANALYZE` to observe query plan details. This example shows a query where JIT is not applied due to its low estimated cost.

```sql
=# EXPLAIN ANALYZE SELECT SUM(relpages) FROM pg_class;
                                                 QUERY PLAN
-------------------------------------------------------------------​------------------------------------------
 Aggregate  (cost=16.27..16.29 rows=1 width=8) (actual time=0.303..0.303 rows=1.00 loops=1)
   Buffers: shared hit=14
   ->  Seq Scan on pg_class  (cost=0.00..15.42 rows=342 width=4) (actual time=0.017..0.111 rows=356.00 loops=1)
         Buffers: shared hit=14
 Planning Time: 0.116 ms
 Execution Time: 0.365 ms
```

--------------------------------

### Check SELinux status with sestatus

Source: https://www.postgresql.org/docs/current/sepgsql.html

Verify that SELinux is enabled and in enforcing mode on the host system before installing the module.

```shell
$ sestatus
SELinux status:                 enabled
SELinuxfs mount:                /selinux
Current mode:                   enforcing
Mode from config file:          enforcing
Policy version:                 24
Policy from config file:        targeted

```

--------------------------------

### pgbench Option: -M / --protocol

Source: https://www.postgresql.org/docs/current/pgbench.html

Specifies the protocol to use for submitting queries to the server: `simple`, `extended`, or `prepared`. Default is `simple`.

```APIDOC
## COMMAND-LINE OPTION -M / --protocol

### Description
Specifies the protocol to use for submitting queries to the PostgreSQL server.
- `simple`: Uses the simple query protocol.
- `extended`: Uses the extended query protocol.
- `prepared`: Uses the extended query protocol with prepared statements, reusing parse analysis results for faster execution after the first iteration.
The default protocol is `simple`.

### Method
Command-line argument

### Endpoint
pgbench

### Parameters
#### Path Parameters
- No path parameters.

#### Query Parameters
- No query parameters.

#### Request Body
- **querymode** (string) - Required - The query protocol to use: `simple`, `extended`, or `prepared`.

### Request Example
```bash
pgbench -M prepared
pgbench --protocol=extended
```

### Response
#### Success Response (0)
- No direct API response. The option configures the query submission method.

#### Response Example
No direct API response.
```

--------------------------------

### Reset pg_stat_statements Statistics

Source: https://www.postgresql.org/docs/current/pgstatstatements.html

Use this command to reset all collected statistics. This is useful for starting fresh performance analysis.

```sql
SELECT pg_stat_statements_reset();
```

--------------------------------

### PostgreSQL EXPLAIN with AND Condition and Bitmap Indexes

Source: https://www.postgresql.org/docs/current/using-explain.html

This example demonstrates how the PostgreSQL planner uses a BitmapAnd operation to combine results from two separate index scans for a query with an AND condition. It shows the cost and row estimates for each step.

```SQL
EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 100 AND unique2 > 9000;

                                     QUERY PLAN
-------------------------------------------------------------------​------------------
 Bitmap Heap Scan on tenk1  (cost=25.07..60.11 rows=10 width=244)
   Recheck Cond: ((unique1 < 100) AND (unique2 > 9000))
   ->  BitmapAnd  (cost=25.07..25.07 rows=10 width=0)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..5.04 rows=100 width=0)
               Index Cond: (unique1 < 100)
         ->  Bitmap Index Scan on tenk1_unique2  (cost=0.00..19.78 rows=999 width=0)
               Index Cond: (unique2 > 9000)
```

--------------------------------

### Find substring position in PostgreSQL

Source: https://www.postgresql.org/docs/current/functions-string.html

Returns the first starting index of a substring within a string, or zero if not found.

```sql
strpos('high', 'ig')
```

--------------------------------

### now Function

Source: https://www.postgresql.org/docs/current/functions-datetime.html

Returns the current date and time as a timestamp with time zone. The value is fixed at the start of the current transaction.

```APIDOC
## now

### Description
Current date and time (start of current transaction).

### Signature
```
now() → timestamp with time zone
```

### Parameters
None

### Usage Example
```sql
now()
```

### Result
```
2019-12-23 14:39:53.662522-05
```
```

--------------------------------

### CREATE TABLE Parameters Reference

Source: https://www.postgresql.org/docs/current/sql-createforeigntable.html

Complete reference for PostgreSQL CREATE TABLE statement parameters and clauses. This documentation covers table creation options, column specifications, inheritance, partitioning, and constraint definitions used when creating new tables in PostgreSQL.

```APIDOC
# PostgreSQL CREATE TABLE Parameters

## IF NOT EXISTS

**Description**: Do not throw an error if a relation with the same name already exists. A notice is issued in this case.

**Note**: There is no guarantee that the existing relation is anything like the one that would have been created.

---

## table_name

**Type**: Identifier

**Description**: The name (optionally schema-qualified) of the table to be created.

---

## column_name

**Type**: Identifier

**Description**: The name of a column to be created in the new table.

---

## data_type

**Type**: Data Type Specification

**Description**: The data type of the column. This can include array specifiers. For more information on the data types supported by PostgreSQL, refer to Chapter 8.

---

## COLLATE collation

**Description**: The COLLATE clause assigns a collation to the column (which must be of a collatable data type). If not specified, the column data type's default collation is used.

---

## INHERITS (parent_table [, ... ])

**Description**: The optional INHERITS clause specifies a list of tables from which the new foreign table automatically inherits all columns. Parent tables can be plain tables or foreign tables. See the similar form of CREATE TABLE for more details.

---

## PARTITION OF parent_table { FOR VALUES partition_bound_spec | DEFAULT }

**Description**: This form can be used to create the foreign table as partition of the given parent table with specified partition bound values. See the similar form of CREATE TABLE for more details.

**Note**: It is currently not allowed to create the foreign table as a partition of the parent table if there are UNIQUE indexes on the parent table. (See also ALTER TABLE ATTACH PARTITION.)

---

## LIKE source_table [like_option ... ]

**Description**: The LIKE clause specifies a table from which the new table automatically copies all column names, their data types, and their not-null constraints.

**Key Differences from INHERITS**:
- The new table and original table are completely decoupled after creation is complete
- Changes to the original table will not be applied to the new table
- It is not possible to include data of the new table in scans of the original table
- Columns and constraints copied by LIKE are not merged with similarly named columns and constraints
- If the same name is specified explicitly or in another LIKE clause, an error is signaled

### LIKE Options

#### INCLUDING COMMENTS
- Comments for the copied columns and constraints will be copied
- Default behavior is to exclude comments, resulting in the copied columns and constraints in the new table having no comments

#### INCLUDING CONSTRAINTS
- CHECK constraints will be copied
- No distinction is made between column constraints and table constraints
- Not-null constraints are always copied to the new table

#### INCLUDING DEFAULTS
- Default expressions for the copied column definitions will be copied
- Otherwise, default expressions are not copied, resulting in the copied columns in the new table having null defaults
- Note: Copying defaults that call database-modification functions, such as nextval, may create a functional linkage between the original and new tables

#### INCLUDING GENERATED
- Any generation expressions of copied column definitions will be copied
- By default, new columns will be regular base columns

#### INCLUDING STATISTICS
- Extended statistics are copied to the new table

#### INCLUDING ALL
- INCLUDING ALL is an abbreviated form selecting all the available individual options
- It could be useful to write individual EXCLUDING clauses after INCLUDING ALL to select all but some specific options

---

## CONSTRAINT constraint_name

**Type**: Identifier

**Description**: An optional name for a column or table constraint. If the constraint is violated, the constraint name is present in error messages, so constraint names like "col must be positive" can be used to communicate helpful constraint information to client applications.

**Note**: Double-quotes are needed to specify constraint names that contain spaces. If a constraint name is not specified, the system generates a name.

---

## NOT NULL [ NO INHERIT ]

**Description**: The column is not allowed to contain null values.

**NO INHERIT**: A constraint marked with NO INHERIT will not propagate to child tables.

---

## NULL

**Description**: The column is allowed to contain null values. This is the default.

**Note**: This clause is only provided for compatibility with non-standard SQL databases. Its use is discouraged in new applications.

---

## CHECK (expression) [ NO INHERIT ]

**Description**: Specifies a CHECK constraint on a column or table. The expression must evaluate to a boolean value.

**NO INHERIT**: A constraint marked with NO INHERIT will not propagate to child tables.
```

--------------------------------

### Add element to the start of an array

Source: https://www.postgresql.org/docs/current/functions-array.html

Prepends a single element to the beginning of an array. This function is equivalent to the || operator.

```sql
array_prepend(1, ARRAY[2,3])
```

--------------------------------

### Start an ECPG declare section

Source: https://www.postgresql.org/docs/current/ecpg-variables.html

Marks the beginning of a block where C variables used in SQL must be declared.

```C
EXEC SQL BEGIN DECLARE SECTION;
```

--------------------------------

### GET pg_stats_ext_exprs View

Source: https://www.postgresql.org/docs/current/view-pg-stats-ext-exprs.html

Retrieves information about expressions included in extended statistics objects from the `pg_stats_ext_exprs` system view.

```APIDOC
## GET pg_stats_ext_exprs View

### Description
The view `pg_stats_ext_exprs` provides access to information about all expressions included in extended statistics objects, combining information stored in the `pg_statistic_ext` and `pg_statistic_ext_data` catalogs. This view allows access only to rows of `pg_statistic_ext` and `pg_statistic_ext_data` that correspond to tables the user owns, and therefore it is safe to allow public read access to this view. It is designed to present the information in a more readable format than the underlying catalogs.

### Method
SELECT (View Access)

### Endpoint
pg_stats_ext_exprs

### Response
#### Success Response (200)
- **schemaname** (name) - Name of schema containing table
- **tablename** (name) - Name of table the statistics object is defined on
- **statistics_schemaname** (name) - Name of schema containing extended statistics object
- **statistics_name** (name) - Name of extended statistics object
- **statistics_owner** (name) - Owner of the extended statistics object
- **expr** (text) - Expression included in the extended statistics object
- **inherited** (bool) - If true, the stats include values from child tables, not just the values in the specified relation
- **null_frac** (float4) - Fraction of expression entries that are null
- **avg_width** (int4) - Average width in bytes of expression's entries
- **n_distinct** (float4) - If greater than zero, the estimated number of distinct values in the expression. If less than zero, the negative of the number of distinct values divided by the number of rows.
- **most_common_vals** (anyarray) - A list of the most common values in the expression. (Null if no values seem to be more common than any others.)
- **most_common_freqs** (float4[]) - A list of the frequencies of the most common values, i.e., number of occurrences of each divided by total number of rows. (Null when `most_common_vals` is.)
- **histogram_bounds** (anyarray) - A list of values that divide the expression's values into groups of approximately equal population. The values in `most_common_vals`, if present, are omitted from this histogram calculation. (This expression is null if the expression data type does not have a `<` operator or if the `most_common_vals` list accounts for the entire population.)
- **correlation** (float4) - Statistical correlation between physical row ordering and logical ordering of the expression values. This ranges from -1 to +1. (This expression is null if the expression's data type does not have a `<` operator.)
- **most_common_elems** (anyarray) - A list of non-null element values most often appearing within values of the expression. (Null for scalar types.)
- **most_common_elem_freqs** (float4[]) - A list of the frequencies of the most common element values, i.e., the fraction of rows containing at least one instance of the given value. Two or three additional values follow the per-element frequencies; these are the minimum and maximum of the preceding per-element frequencies, and optionally the frequency of null elements. (Null when `most_common_elems` is.)
- **elem_count_histogram** (float4[]) - A histogram of the counts of distinct non-null element values within the values of the expression, followed by the average number of distinct non-null elements. (Null for scalar types.)

#### Response Example
```json
{
  "schemaname": "public",
  "tablename": "orders",
  "statistics_schemaname": "pg_catalog",
  "statistics_name": "orders_total_expr_stats",
  "statistics_owner": "app_user",
  "expr": "quantity * price",
  "inherited": false,
  "null_frac": 0.01,
  "avg_width": 8,
  "n_distinct": 5000.0,
  "most_common_vals": ["100.00", "50.00"],
  "most_common_freqs": [0.05, 0.03],
  "histogram_bounds": ["10.00", "25.00", "75.00", "200.00"],
  "correlation": 0.65,
  "most_common_elems": null,
  "most_common_elem_freqs": null,
  "elem_count_histogram": null
}
```
```

--------------------------------

### Perform dynamic domain transitions with sepgsql_setcon

Source: https://www.postgresql.org/docs/current/sepgsql.html

Switch the current SELinux security context using sepgsql_setcon. Transitions are restricted by the security policy to prevent privilege escalation.

```sql
regression=# select sepgsql_getcon();
                    sepgsql_getcon
-------------------------------------------------------
 unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
(1 row)

regression=# SELECT sepgsql_setcon('unconfined_u:unconfined_r:unconfined_t:s0-s0:c1.c4');
 sepgsql_setcon
----------------
 t
(1 row)

regression=# SELECT sepgsql_setcon('unconfined_u:unconfined_r:unconfined_t:s0-s0:c1.c1023');
ERROR:  SELinux: security policy violation
```

--------------------------------

### CREATE TABLE - Basic Syntax

Source: https://www.postgresql.org/docs/current/sql-createtable.htm

Defines a new table with columns and constraints. This is the standard form of CREATE TABLE that allows specification of column definitions, table constraints, inheritance, partitioning, and storage options.

```APIDOC
## CREATE TABLE

### Description
Defines a new table in the database with specified columns, constraints, and optional features such as partitioning and inheritance.

### Syntax
```
CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name (
  { column_name data_type [ STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT } ] [ COMPRESSION compression_method ] [ COLLATE collation ] [ column_constraint [ ... ] ]
    | table_constraint
    | LIKE source_table [ like_option ... ] }
    [, ... ]
)
[ INHERITS ( parent_table [, ... ] ) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]
```

### Parameters

#### Table Options
- **GLOBAL | LOCAL** - Optional - Scope modifier for temporary tables (GLOBAL or LOCAL)
- **TEMPORARY | TEMP** - Optional - Creates a temporary table that is automatically dropped at end of session
- **UNLOGGED** - Optional - Creates an unlogged table that is not written to WAL
- **IF NOT EXISTS** - Optional - Do not throw an error if table already exists
- **table_name** - Required - Name of the table to create

#### Column Definition
- **column_name** - Required - Name of the column
- **data_type** - Required - Data type of the column
- **STORAGE** - Optional - Storage strategy: PLAIN, EXTERNAL, EXTENDED, MAIN, or DEFAULT
- **COMPRESSION** - Optional - Compression method for the column
- **COLLATE** - Optional - Collation for the column
- **column_constraint** - Optional - Constraints applied to the column (NOT NULL, UNIQUE, PRIMARY KEY, CHECK, DEFAULT, GENERATED, REFERENCES)

#### Table-Level Options
- **INHERITS** - Optional - Specifies parent table(s) for inheritance
- **PARTITION BY** - Optional - Partitioning strategy: RANGE, LIST, or HASH with partition key columns
- **USING** - Optional - Index method for constraints
- **WITH** - Optional - Storage parameters as key-value pairs
- **WITHOUT OIDS** - Optional - Do not include OID column
- **ON COMMIT** - Optional - Action on transaction commit: PRESERVE ROWS, DELETE ROWS, or DROP
- **TABLESPACE** - Optional - Tablespace where table will be stored

### Column Constraints
- **NOT NULL [ NO INHERIT ]** - Column must have a value
- **NULL** - Column may have NULL values (default)
- **CHECK ( expression ) [ NO INHERIT ]** - Values must satisfy the expression
- **DEFAULT default_expr** - Default value for the column
- **GENERATED ALWAYS AS ( generation_expr ) [ STORED | VIRTUAL ]** - Generated column
- **GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ]** - Identity column
- **UNIQUE [ NULLS [ NOT ] DISTINCT ] index_parameters** - Values must be unique
- **PRIMARY KEY index_parameters** - Unique identifier for rows
- **REFERENCES reftable [ ( refcolumn ) ] [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ] [ ON DELETE referential_action ] [ ON UPDATE referential_action ]** - Foreign key constraint

### Table Constraints
- **CHECK ( expression ) [ NO INHERIT ]** - Constraint on one or more columns
- **NOT NULL column_name [ NO INHERIT ]** - Column must not be NULL
- **UNIQUE [ NULLS [ NOT ] DISTINCT ] ( column_name [, ... ] ) index_parameters** - Unique constraint on columns
- **PRIMARY KEY ( column_name [, ... ] ) index_parameters** - Primary key constraint
- **EXCLUDE [ USING index_method ] ( exclude_element WITH operator [, ... ] ) index_parameters [ WHERE ( predicate ) ]** - Exclusion constraint
- **FOREIGN KEY ( column_name [, ... ] ) REFERENCES reftable [ ( refcolumn [, ... ] ) ] [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ] [ ON DELETE referential_action ] [ ON UPDATE referential_action ]** - Foreign key constraint

### LIKE Options
- **INCLUDING | EXCLUDING** - Include or exclude specific properties
- **COMMENTS | COMPRESSION | CONSTRAINTS | DEFAULTS | GENERATED | IDENTITY | INDEXES | STATISTICS | STORAGE | ALL** - Properties to include/exclude from source table

### Partition Bound Specification
- **IN ( partition_bound_expr [, ...] )** - LIST partition bounds
- **FROM ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] ) TO ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] )** - RANGE partition bounds
- **WITH ( MODULUS numeric_literal, REMAINDER numeric_literal )** - HASH partition bounds

### Referential Actions
- **NO ACTION** - Produce error if foreign key is referenced
- **RESTRICT** - Prevent deletion of referenced row
- **CASCADE** - Delete referencing rows
- **SET NULL** - Set referencing columns to NULL
- **SET DEFAULT** - Set referencing columns to default values
```

--------------------------------

### GET /pg_stat_all_indexes

Source: https://www.postgresql.org/docs/current/monitoring-stats.html

Retrieves statistics for each index in the current database, showing access counts and tuple retrieval data.

```APIDOC
## GET /pg_stat_all_indexes

### Description
Returns one row for each index in the current database, showing statistics about accesses to that specific index.

### Method
GET

### Endpoint
pg_stat_all_indexes

### Parameters
#### Path Parameters
None

#### Query Parameters
None

### Request Example
SELECT * FROM pg_stat_all_indexes;

### Response
#### Success Response (200)
- **relid** (oid) - OID of the table for this index
- **indexrelid** (oid) - OID of this index
- **schemaname** (name) - Name of the schema this index is in
- **relname** (name) - Name of the table for this index
- **indexrelname** (name) - Name of this index
- **idx_scan** (bigint) - Number of index scans initiated on this index
- **last_idx_scan** (timestamp with time zone) - The time of the last scan on this index
- **idx_tup_read** (bigint) - Number of index entries returned by scans on this index
- **idx_tup_fetch** (bigint) - Number of live table rows fetched by simple index scans

#### Response Example
{
  "relid": 16384,
  "indexrelid": 16390,
  "schemaname": "public",
  "relname": "users",
  "indexrelname": "users_pkey",
  "idx_scan": 500,
  "last_idx_scan": "2023-10-27T10:00:00Z",
  "idx_tup_read": 1000,
  "idx_tup_fetch": 950
}
```

--------------------------------

### Load and Configure auto_explain Module in PostgreSQL

Source: https://www.postgresql.org/docs/current/auto-explain.html

Load the auto_explain module and configure it to log all queries with analysis enabled. Set log_min_duration to 0 to log all queries regardless of execution time.

```sql
postgres=# LOAD 'auto_explain';
postgres=# SET auto_explain.log_min_duration = 0;
postgres=# SET auto_explain.log_analyze = true;
postgres=# SELECT count(*)
           FROM pg_class, pg_index
           WHERE oid = indrelid AND indisunique;
```

--------------------------------

### Get column data type OID with PQftype

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Returns the internal OID for the column's data type.

```c
Oid PQftype(const PGresult *res,
            int column_number);
```

--------------------------------

### Get source table column index with PQftablecol

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Returns the column's index within its source table.

```c
int PQftablecol(const PGresult *res,
                int column_number);
```

--------------------------------

### Open cursor with input SQLDA parameters

Source: https://www.postgresql.org/docs/current/ecpg-descriptors.html

Execute the prepared statement by opening the cursor and passing the input SQLDA descriptor containing the parameter values.

```C
    /* Open a cursor with input parameters. */
    EXEC SQL OPEN cur1 USING DESCRIPTOR sqlda2;
```

--------------------------------

### COMMAND initdb

Source: https://www.postgresql.org/docs/current/app-initdb.htm

The `initdb` command is a utility for creating a new PostgreSQL database cluster. It sets up the necessary file system structure, shared catalog tables, and default databases, allowing for initial configuration of locale and character set encoding.

```APIDOC
## COMMAND initdb

### Description
The `initdb` command creates a new PostgreSQL database cluster. This involves setting up the necessary directories, generating shared catalog tables, and creating the default databases (`postgres`, `template1`, and `template0`). It also allows for initial configuration of locale and character set encoding.

### Method
CLI Command

### Command
initdb

### Parameters
#### Command Options
- **--pgdata | -D** (string) - Required - Specifies the directory where the database cluster will be stored.
- **--allow-group-access** (flag) - Optional - Allows any user in the same group as the cluster owner to read files in the cluster. This is useful for performing backups as a non-privileged user.
- **--locale** (string) - Optional - Sets the default locale for the cluster. By default, `initdb` uses the `libc` locale provider.
- **--lc-*** (string) - Optional - Sets values for individual locale categories (e.g., `--lc-collate`, `--lc-ctype`).
- **--icu-locale** (string) - Optional - Specifies the specific ICU locale ID to apply when `--locale-provider=icu` is used.
- **--locale-provider** (string) - Optional - Specifies the locale provider to use. Options include `libc` (default) or `icu` (requires ICU support).
- **--encoding** (string) - Optional - Sets the default character set encoding for the cluster.

### Request Example
```bash
initdb -D /usr/local/pgsql/data --locale=en_US.UTF-8 --encoding=UTF8
```

### Response
#### Success Response (0)
The command exits with status 0 on success. The output typically includes chosen locale settings and confirmation of cluster creation.

#### Response Example
```text
The files belonging to this database system will be owned by user \"postgres\".
This user must also own the server process.

The database cluster will be initialized with locale \"en_US.UTF-8\".
The default database encoding has been set to \"UTF8\".
The default text search configuration will be set to \"english\".

Data page checksums are disabled.

creating directory /usr/local/pgsql/data ... ok
creating subdirectories ... ok
selecting dynamic shared memory implementation ... posix
selecting default max_connections ... 100
selecting default shared_buffers ... 128MB
selecting default time zone ... America/New_York
creating configuration files ... ok
running bootstrap script ... ok
performing post-bootstrap initialization ... ok
syncing data to disk ... ok

initdb: warning: enabling \"trust\" authentication for local connections
You can change this by editing pg_hba.conf or using the option -A, or --auth-local and --auth-host, the next time you run initdb.
initdb: initializing database system complete; see log for details
```
```

--------------------------------

### Get column index with PQfnumber

Source: https://www.postgresql.org/docs/current/libpq-exec.html

Returns the index for a given name, handling SQL identifier case rules.

```c
int PQfnumber(const PGresult *res,
              const char *column_name);
```