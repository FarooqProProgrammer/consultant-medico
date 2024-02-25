import re
import random
import string
import os

def generate_css_class(used_classes):
    """Generate a random unique CSS class name."""
    css_class = ''.join(random.choices(string.ascii_lowercase, k=6))
    while css_class in used_classes:
        css_class = ''.join(random.choices(string.ascii_lowercase, k=6))
    return css_class

def extract_inline_styles(html_content):
    """Extract inline style tags and their content from HTML."""
    return re.findall(r'<style>(.*?)</style>', html_content, re.DOTALL)

def extract_style_rules(inline_styles):
    """Extract CSS rules from inline style tags."""
    style_rules = []
    for style in inline_styles:
        style_rules.extend(re.findall(r'([^{}]+)\s*\{([^{}]+)\}', style))
    return style_rules

def write_to_css_file(style_rules):
    """Write CSS rules to a CSS file."""
    css_file_path = 'css/style.css'
    if os.path.exists(css_file_path):
        os.remove(css_file_path)
    
    used_classes = set()
    with open(css_file_path, 'a') as css_file:
        for selector, rules in style_rules:
            css_class = generate_css_class(used_classes)
            used_classes.add(css_class)
            css_file.write(f".{css_class} {{{rules}}}\n")
            yield css_class, selector

def update_html_with_classes(html_content, css_classes):
    """Update HTML tags with generated CSS classes."""
    updated_html = html_content
    for css_class, selector in css_classes:
        updated_html = re.sub(selector, f'{selector} class="{css_class}"', updated_html)
    return updated_html

def main():
    # Read HTML file
    with open('index.html', 'r') as html_file:
        html_content = html_file.read()

    # Extract inline style tags
    inline_styles = extract_inline_styles(html_content)

    # Extract CSS rules from inline style tags
    style_rules = extract_style_rules(inline_styles)

    # Write CSS rules to CSS file and get generated CSS classes
    css_classes = list(write_to_css_file(style_rules))

    # Update HTML tags with generated CSS classes
    updated_html = update_html_with_classes(html_content, css_classes)

    # Write updated HTML content to file
    with open('index_updated.html', 'w') as updated_html_file:
        updated_html_file.write(updated_html)

if __name__ == "__main__":
    main()
