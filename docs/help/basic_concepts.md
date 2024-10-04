[Home](../) > [Help pages](index) > Basic concepts

---

# Basic concepts

## The Book hierarchy

### Parts

A novel is expected to be divided into chapters and sections. Parts are
optional; technically they are first level chapters. However, in the
*mdnovel* project tree they are on the same level as the chapters, but
they produce a heading one level above. Thus, parts are mainly for
inserting first level headings between the chapters, if needed.

---

**Hint**

You can convert chapters into parts and vice versa by simply [changing
the level](tree_context_menu#change-level).

---

### Chapters

A *mdnovel* project must at least have one chapter. In the exported
documents, regular chapters have a second level heading.

For *mdnovel*, the chapters only serve as containers for sections to
which the actual dramaturgical function is assigned. This is why there
are only a few [chapter properties](chapter_view) to be set.

### Sections

All body text of a novel in *mdnovel* belongs to sections. Sections
can be scenes, pieces of exposition, descriptions, narrative
summaries---it is entirely up to you how you divide your text into
sections. There is a variety of [metadata for
sections](section_view) for your free use.

In the text body of the exported documents, sections are separated by
section dividers by default, like so:

`* * *`

However, if you need more fragmented sections when plotting and
organizing than the reader should see later, you can also [append
sections](section_view#append-to-previous-section) to each other as
new paragraphs with no section divider inbetween.

## Part/chapter/section types

Each part, chapter, and section is of a type that can be changed via
context menu or Part/Chapter/Section menu. The type can be *Normal* or
*Unused*.

Normal

:  - "Normal" type parts, chapters, and sections are counted. The totals
     are displayed in the status bar.
   - "Normal" type sections are exported to the manuscript and included in
     the word count.
   - "Normal" type parts and chapters can have subelements of each type.
   - "Normal" type tree elements are color coded according to the [coloring
     mode settings](view_menu#coloring-mode).

Unused

:  You can mark parts, chapters, and sections as unused to exclude them
   from word count totals and export.
   
   - The subelements of unused parts and chapters are unused as well.
   - If you mark a section "Unused", its properties are preserved.
   - Unused tree elements are displayed in gray.

## Section completion status

You can assign a status to each "Normal" type section via context menu
or Section menu. You can choose between Outline\*, *Draft*, *1st Edit*,
*2nd Edit*, and *Done*.

- You can choose a [coloring mode](view_menu#coloring-mode) to
  display sections in different colors depending on their completion
  status.
- Optionally, you can declare one of the status to be the current [work
  phase](book_view#writing-progress), and choose a [coloring
  mode](view_menu#coloring-mode) that highlights sections that are
  behind schedule.
- Newly created sections are set to "Outline" by default.
- Word counts by status appear in the [Book
  properties](book_view#writing-pogress).

------------------------------------------------------------------------

## Characters and story world

You can define characters, locations, and items, and you can relate them
to sections to keep track of their place in the story. There is also
some metadata stored with *mdnovel*, mainly as a quick reference that
might come in handy when writing or editing.

---

**Note**

*mdnovel* is not meant as a tool for extensive world building. For
this, there is a plethora of dedicated applications, online and offline
wikis, and notetaking software. However, *mdnovel* offers the option
of linking images and files with the characters, locations, and items to
facilitate access if your external application allows this.

---

---

**Important**

If you want to assign **viewpoint characters** to your sections, you
first have to [create](characters_menu#add) the characters that
come into question.

---

