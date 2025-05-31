import os
import shutil
import sys
from copystatic import copy_files_recursive
from markdown_block import markdown_to_html_node
from markdown import extract_title
static_dir = "static"
public_dir = "public"
content_dir = "content"
template_path = "template.html"
def main():
    
    if os.path.exists(static_dir):
        shutil.rmtree(public_dir)
        
        print("Copying static files...")
        copy_files_recursive(static_dir, public_dir)
        print("Static files copied successfully.")

    generate_pages_recursive(content_dir, template_path, public_dir)
    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating pages from {from_path} to {dest_path} using template {template_path}")
    with open(template_path, "r") as template_file:
        template = template_file.read()
    
    with open(from_path, "r") as markdown_file:
        markdown_content = markdown_file.read()
    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    html_node = markdown_to_html_node(markdown_content)
    html_content = template.replace("{{ Content }}", html_node.to_html())

    with open(dest_path, "w") as output_file:
        output_file.write(html_content)
    print("Page generated successfully.")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(from_path):
            newFilename = filename.split(".")[0] + ".html"
            dest_path = os.path.join(dest_dir_path, newFilename)
            print(f" * {from_path} -> {dest_path}")
            generate_page(from_path, template_path, dest_path)
        else:
            dest_path = os.path.join(dest_dir_path, filename)
            os.mkdir(dest_path)
            generate_pages_recursive(from_path, template_path, dest_path)

    
main()