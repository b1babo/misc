#!/usr/bin/env python3

import click
import lief
# import pathlib
import os




def change_glibc(bin,libc,ld,out):

    binary = lief.parse(bin)

    libc_name = None
    for i in binary.libraries:
        if "libc.so.6" in i:
            libc_name = i
            break

    if libc_name is None:
        click.echo("No libc linked. Exiting.")

    click.echo("Current ld.so:")
    click.echo("Path: {}".format(binary.interpreter))
    click.echo()
    libc_path = os.path.dirname(libc)
    # libc_path = str(pathlib.Path(str(libc)).parent)

    binary.interpreter = str(ld)
    click.echo("New ld.so:")
    click.echo("Path: {}".format(binary.interpreter))
    click.echo()

    binary += lief.ELF.DynamicEntryRunPath(libc_path)
    click.echo("Adding RUNPATH:")
    click.echo("Path: {}".format(libc_path))
    click.echo()

    click.echo("Writing new binary {}".format(out))
    click.echo("Please rename {} to {}/libc.so.6.".format(
        libc, libc_path
    ))
    binary.write(out)







@click.command(
    help="Change the linked glibc of an ELF binary."
)
@click.argument("bin", type=click.Path(exists=True))
@click.argument("version", type=str)
@click.option("--disable-tcache","disable_tcache",flag_value="notcache",default="tcache",is_flag=False)
@click.option("--i686","i686",flag_value="i686",default="x64",is_flag=False)
@click.option("--extra","extra",flag_value=True,default=False,is_flag=False)
# @click.argument("libc", type=click.Path(exists=True, resolve_path=True))
# @click.argument("ld", type=click.Path(exists=True, resolve_path=True))
# @click.argument("out", type=click.Path())
def cli(bin, version, disable_tcache,i686,extra):

    if extra:
        i686 = "amd64"

        lib_dir = f"/home/bibabo/glibc-all-in-one/libs/{version}-0ubuntu11.3_{i686}"
                    
    else:
        lib_dir = f"/home/bibabo/how2heap/glibc_versions/{version}/{i686}_{disable_tcache}/lib"


    # print(lib_dir)
    libc = os.path.join(lib_dir,f"libc-{version}.so")
    ld = os.path.join(lib_dir,f"ld-{version}.so")
    bin = os.path.abspath(bin)
    out_file_name = f"{os.path.basename(bin)}_{i686}_{disable_tcache}"
    out_file_path = os.path.join(os.path.dirname(bin),out_file_name)

    change_glibc(bin,libc,ld,out_file_path)

if __name__ == "__main__":
    cli()