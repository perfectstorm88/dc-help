# -- coding:utf8 --
import argparse
#添加子命令函数
def foo(args):
    print (args.x * args.y)
 
def bar(args):
    print ('((%s))' %args.z)
 
#创建最上层解析器
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='subcommands',
                                    description='valid subcommands',
                                    help='additional help',
                                    dest='subparser_name')
 
#创建子解析器 'foo'
parser_foo = subparsers.add_parser('foo')
parser_foo.add_argument('-x', type=int, default=1)
parser_foo.add_argument('y', type=float)
parser_foo.set_defaults(func=foo) #将函数foo 与子解析器foo绑定
 
#创建子解析器‘bar'
parser_bar = subparsers.add_parser('bar')
parser_bar.add_argument('z')
parser_bar.set_defaults(func=bar) #将函数bar与子解析器bar绑定
 
args = parser.parse_args('foo 1 -x 2'.split())
#Namespace(func=<function foo at 0xd6ae60>, subparser_name='foo', x=2, y=1.0)
args.func(args)
#2.0
 
args = parser.parse_args('bar xyzyz'.split())
#Namespace(func=<function bar at 0xd6aed8>, subparser_name='bar', z='xyzyz')
args.func(args)
#((xyzyz))
 
parser.parse_args(['-h'])
#usage: subparser_example.py [-h] {foo,bar} ...
#
#optional arguments:
#  -h, --help  show this help message and exit
#
#subcommands:
#  valid subcommands
#
#  {foo,bar}   additional help

