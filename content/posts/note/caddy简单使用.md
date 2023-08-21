---
title: "caddy简单使用"
date: "2023-08-21"
description: "caddy简单使用"
featured : false
categories: ["notes"]
tags: [ "notes" ]
series: [ "notes" ]
images: []
---
- [1. caddy 简介](#1-caddy-简介)
- [2. caddy VS. nginx](#2-caddy-vs-nginx)
- [3. caddy 简单使用](#3-caddy-简单使用)
  - [1. 安装](#1-安装)
- [4. Run the daemon](#4-run-the-daemon)
- [5. 创建一个配置](#5-创建一个配置)
- [6. 使用caddy file](#6-使用caddy-file)

## 1. caddy 简介
官方文档：https://caddyserver.com/docs/

我认为caddy 就是类似于nginx 的角色，并且其没有依赖，丰富的平台支持性，简洁的使用方式，完全可以用于在某些场景替换nginx

nginx VS. caddy：https://cloudinfrastructureservices.co.uk/caddy-vs-nginx-which-web-server-is-better/

## 2. caddy VS. nginx
GPT:
比较Caddy和Nginx的方面：

配置简单性： Caddy以其简洁的配置语法而闻名，通过Caddyfile配置文件，用户可以轻松地完成各种任务，包括自动配置HTTPS、反向代理、静态文件服务等。相比之下，Nginx的配置文件语法可能相对复杂一些。

自动HTTPS： Caddy内置了自动获取和管理SSL证书的功能，可以在几乎不需要额外配置的情况下实现自动化的HTTPS支持。而Nginx需要手动设置和配置SSL证书。

插件生态系统： Caddy具有丰富的插件生态系统，可以通过插件扩展功能。Nginx也有很多模块和插件，但配置和管理可能需要更多的技术知识。

性能： 在性能方面，Nginx通常被认为是高性能的Web服务器，适用于处理大量的并发连接。Caddy也具备良好的性能，但在处理大规模负载时，Nginx可能会稍微更有优势。

学习曲线： 由于Caddy的简单配置和自动化特性，对于初学者来说，上手和学习可能会更容易。而Nginx的配置可能需要一些时间来理解和掌握。

需要注意的是，选择Caddy还是Nginx取决于你的需求和经验水平。如果你需要更高级的配置选项、对性能要求很高，或者已经熟悉Nginx，那么Nginx可能更适合你。如果你想要一个简单、自动化的解决方案，并且不需要太多复杂的配置，Caddy可能是一个更好的选择。


## 3. caddy 简单使用

### 1. 安装
caddy 支持很多平台，文档：https://caddyserver.com/docs/install

**Official**:

Static binaries
Debian, Ubuntu, Raspbian packages
Fedora, RedHat, CentOS packages
Arch Linux, Manjaro, Parabola packages
Docker image
Our official packages come only with the standard modules. If you need third-party plugins, build from source with xcaddy or use our download page.

**Community-maintained**:

Homebrew (Mac)
Chocolatey (Windows)
Scoop (Windows)
Webi
Ansible
Termux
Nix/Nixpkgs/NixOS

我这里使用scoop 在windows 平添安装caddy

`scoop install caddy`
```
Scoop was updated successfully!
Installing 'caddy' (2.7.4) [64bit] from main bucket
caddy_2.7.4_windows_amd64.zip (14.1 MB) [===========================================================] 100%    
Checking hash of caddy_2.7.4_windows_amd64.zip ... ok.
Extracting caddy_2.7.4_windows_amd64.zip ... done.
Linking D:\scoop\apps\caddy\current => D:\scoop\apps\caddy\2.7.4
Creating shim for 'caddy'.
'caddy' (2.7.4) was installed successfully!

```

caddy 的子命令相当多：
```
(base) PS D:\Projects\windmill\frontend> caddy
Caddy is an extensible server platform written in Go.

At its core, Caddy merely manages configuration. Modules are plugged      
in statically at compile-time to provide useful functionality. Caddy's    
standard distribution includes common modules to serve HTTP, TLS,
and PKI applications, including the automation of certificates.

To run Caddy, use:

        - 'caddy run' to run Caddy in the foreground (recommended).       
        - 'caddy start' to start Caddy in the background; only do this    
          if you will be keeping the terminal window open until you run   
          'caddy stop' to close the server.

When Caddy is started, it opens a locally-bound administrative socket     
to which configuration can be POSTed via a restful HTTP API (see
https://caddyserver.com/docs/api).

Caddy's native configuration format is JSON. However, config adapters     
can be used to convert other config formats to JSON when Caddy receives   
its configuration. The Caddyfile is a built-in config adapter that is     
popular for hand-written configurations due to its straightforward        
syntax (see https://caddyserver.com/docs/caddyfile). Many third-party     
adapters are available (see https://caddyserver.com/docs/config-adapters).
Use 'caddy adapt' to see how a config translates to JSON.

For convenience, the CLI can act as an HTTP client to give Caddy its      
initial configuration for you. If a file named Caddyfile is in the        
current working directory, it will do this automatically. Otherwise,      
you can use the --config flag to specify the path to a config file.       

Some special-purpose subcommands build and load a configuration file
for you directly from command line input; for example:

        - caddy file-server
        - caddy reverse-proxy
        - caddy respond

These commands disable the administration endpoint because their
configuration is specified solely on the command line.

In general, the most common way to run Caddy is simply:

        $ caddy run

Or, with a configuration file:

        $ caddy run --config caddy.json

If running interactively in a terminal, running Caddy in the
background may be more convenient:

        $ caddy start
        ...
        $ caddy stop

This allows you to run other commands while Caddy stays running.
Be sure to stop Caddy before you close the terminal!

Depending on the system, Caddy may need permission to bind to low
ports. One way to do this on Linux is to use setcap:

        $ sudo setcap cap_net_bind_service=+ep $(which caddy)

Remember to run that command again after replacing the binary.

See the Caddy website for tutorials, configuration structure,
syntax, and module documentation: https://caddyserver.com/docs/

Custom Caddy builds are available on the Caddy download page at:
https://caddyserver.com/download

The xcaddy command can be used to build Caddy from source with or
without additional plugins: https://github.com/caddyserver/xcaddy

Where possible, Caddy should be installed using officially-supported
package installers: https://caddyserver.com/docs/install

Instructions for running Caddy in production are also available:
https://caddyserver.com/docs/running

Usage:
  caddy [command]

Examples:
  $ caddy run
  $ caddy run --config caddy.json
  $ caddy reload --config caddy.json
  $ caddy stop

Available Commands:
  adapt          Adapts a configuration to Caddy's native JSON
  add-package    Adds Caddy packages (EXPERIMENTAL)
  build-info     Prints information about this build
  completion     Generate completion script
  environ        Prints the environment
  file-server    Spins up a production-ready file server
  fmt            Formats a Caddyfile
  hash-password  Hashes a password and writes base64
  help           Help about any command
  list-modules   Lists the installed Caddy modules
  manpage        Generates the manual pages for Caddy commands
  reload         Changes the config of the running Caddy instance
  remove-package Removes Caddy packages (EXPERIMENTAL)
  respond        Simple, hard-coded HTTP responses for development and testing
  reverse-proxy  A quick and production-ready reverse proxy
  run            Starts the Caddy process and blocks indefinitely
  start          Starts the Caddy process in the background and then returns
  stop           Gracefully stops a started Caddy process
  storage        Commands for working with Caddy's storage (EXPERIMENTAL)
  trust          Installs a CA certificate into local trust stores
  untrust        Untrusts a locally-trusted CA certificate
  upgrade        Upgrade Caddy (EXPERIMENTAL)
  validate       Tests whether a configuration file is valid
  version        Prints the version

Flags:
  -h, --help   help for caddy

Use "caddy [command] --help" for more information about a command.

Full documentation is available at:
https://caddyserver.com/docs/command-line
```
## 4. Run the daemon
`caddy run ` to run a daemon

```
(base) PS D:\Projects\windmill\frontend> caddy run
2023/08/21 06:10:38.907 INFO    admin   admin endpoint started  {"address": "localhost:2019", "enforce_origin": false, "origins": ["//localhost:2019", "//[::1]:2019", "//127.0.0.1:2019"]}
2023/08/21 06:10:38.907 INFO    serving initial configuration
```

## 5. 创建一个配置
caddy_conig.demo.json
```json
{
	"apps": {
		"http": {
			"servers": {
				"example": {
					"listen": [":2015"],
					"routes": [
						{
							"handle": [{
								"handler": "static_response",
								"body": "Hello, world!"
							}]
						}
					]
				}
			}
		}
	}
}
```
加载配置：
```bash
$ curl localhost:2019/load \
> -H "Content-Type: application/json" \
> -d @caddy_config.demo.json
```
这时在http://localhost:2019/config/中就可以看到我们的配置了

根据配置文件，我们curl :2015
```
curl localhost:2015
Hello, world!
```
该文档详细介绍了使用json作为服务配置以及使用/load端点来加载配置文件：https://caddyserver.com/docs/quick-starts/api

## 6. 使用caddy file
上述为了显示一个hello world ，工作量非常大

我们使用CaddyFile:

```Caddyfile
:2016

respond "Hello, world! with Caddyfile"
```
然后使用caddy 重新加载该文件：
`caddy adapt --config /path/to/Caddyfile`
```bash
$ caddy adapt --config Caddyfile
{"apps":{"http":{"servers":{"srv0":{"listen":[":2016"],"routes":[{"handle":[{"body":"Hello, world! with Caddyfile","handler":"static_response"}]}]}}}}}
2023/08/21 06:29:21.751 WARN    caddyfile       Caddyfile input is not formatted; run 'caddy fmt --overwrite' 
to fix inconsistencies  {"file": "Caddyfile", "line": 3}
```

这里是使用了caddy 的适配器：配置适配器，将我们的 Caddyfile 转换为 Caddy 的原生 JSON 结构。

~~我们只需要重启一下：caddy stop && caddy run~~
使用reload重载配置
`caddy reload`
```bash
$ curl localhost:2016
Hello, world! with Caddyfile
```

如果我们有多个端点，可以使用大括号包裹
```Caddyfile
localhost {
	respond "Hello, world!"
}

localhost:2016 {
	respond "Goodbye, world!"
}

```

该文档介绍了Caddyfile的常用示例和模式：https://caddyserver.com/docs/caddyfile/patterns
