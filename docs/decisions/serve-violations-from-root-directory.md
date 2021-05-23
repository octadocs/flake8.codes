---
title: Serve violations from root of the website
choices:
  - $id: copy-file
    title: Copy the original file to the root directory
    position: 1
  - $id: use-mkdocs-macros
    title: Use <code>mkdocs-macros</code> to hook into MkDocs <code>on_files</code> event
    position: 2
  - $id: create-mkdocs-plugin
    title: Create an ad-hoc <code>MkDocs</code> plugin to hook into <code>on_files</code> event
    position: 3
excludes:
  - $id: copy-file
    reason: Having such a mess of Markdown files in the <code>docs</code> directory would not be a good idea. A lot of duplication, wasted disk space, and ugly diffs. Does not fit any kind of aesthetic standard.
  - $id: use-mkdocs-macros
    reason: The <code>on_files</code> hook is not supported.
    see-also: https://mkdocs-macros-plugin.readthedocs.io/en/latest/macros/#list-of-hook-functions-within-a-module
---

## Context

I would like to have `WPS123` code description from the latest version of `wemake-python-styleguide` available not only as https://flake8.codes/wemake-python-styleguide/0.15.2/violations/WPS123/ but also as https://flake8.codes/WPS123/.

I feel this would greatly improve the usability of the tool, especially if to create a custom search engine for it in your browser.

## Solutions

Somehow, a file at `docs/wemake-python-styleguide/0.15.2/violations/WPS123.md` must be served as `docs/WPS123.md` in addition to its original serving.

{% set choices = query('
    SELECT ?iri ?title WHERE {
        ?adr :choices ?iri .
        
        ?iri
            octa:title ?title ;
            octa:position ?position .
    } ORDER BY ?position
') %}

<table>
    <thead>
        <tr>
            <th>Choice</th>
            <th>Evaluation</th>
    </thead>
    <tbody>
        {% for choice in choices %}
            <tr>
                <td>{{ choice.title }}</td>
                <td>
                    {% set exclusion = query('
                        SELECT * WHERE {
                            ?adr :excludes ?choice .
                            ?choice :reason ?reason .
                            
                            OPTIONAL {
                                ?choice :see-also ?link .
                            }
                        }
                    ', choice=choice.iri).first %}

                    {% if exclusion %}
                        {{ exclusion.reason }}
                        {% if exclusion.link %}
                            <a href="{{ exclusion.link }}">↪</a>
                        {% endif %}
                    {% endif %}

                    {% set is_decision = query('ASK { ?choice a :Decision . }', choice=choice.iri) %}

                    {% if is_decision %}
                        <strong>This is the decision. ✅</strong>
                    {% endif %}
                </td>
            </tr>
        {% endfor %}
    </tbody>
</table>
