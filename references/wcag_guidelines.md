# WCAG 2.2 Guidelines Reference

This document provides a comprehensive reference for Web Content Accessibility Guidelines (WCAG) 2.2, the international standard for web accessibility.

## Overview

WCAG 2.2 is organized around four main principles (POUR):

1. **Perceivable** - Information and user interface components must be presentable to users in ways they can perceive
2. **Operable** - User interface components and navigation must be operable
3. **Understandable** - Information and the operation of user interface must be understandable
4. **Robust** - Content must be robust enough that it can be interpreted reliably by a wide variety of user agents, including assistive technologies

## Conformance Levels

- **Level A** (Minimum): Basic web accessibility features
- **Level AA** (Standard): Recommended level for most organizations
- **Level AAA** (Enhanced): Highest level of accessibility

## Common WCAG 2.2 Success Criteria

### Perceivable

#### 1.1 Text Alternatives
- **1.1.1 Non-text Content (A)**: Provide text alternatives for non-text content
  - All images need alt text
  - Decorative images should have empty alt=""
  - Complex images need detailed descriptions

#### 1.2 Time-based Media
- **1.2.1 Audio-only and Video-only (A)**: Provide alternatives for audio/video
- **1.2.2 Captions (A)**: Provide captions for all videos with audio
- **1.2.3 Audio Description or Media Alternative (A)**: Provide audio description
- **1.2.4 Captions (Live) (AA)**: Provide captions for live audio
- **1.2.5 Audio Description (AA)**: Provide audio description for video

#### 1.3 Adaptable
- **1.3.1 Info and Relationships (A)**: Structure can be programmatically determined
  - Use semantic HTML (header, nav, main, etc.)
  - Proper heading hierarchy (h1, h2, h3)
  - Use lists for list content
  - Use tables for tabular data
- **1.3.2 Meaningful Sequence (A)**: Content order makes sense
- **1.3.3 Sensory Characteristics (A)**: Don't rely solely on shape, size, location, or sound
- **1.3.4 Orientation (AA)**: Don't restrict to single orientation
- **1.3.5 Identify Input Purpose (AA)**: Identify purpose of input fields

#### 1.4 Distinguishable
- **1.4.1 Use of Color (A)**: Don't use color alone to convey information
- **1.4.2 Audio Control (A)**: Provide way to pause/stop audio
- **1.4.3 Contrast (Minimum) (AA)**: 4.5:1 contrast ratio for text
  - 3:1 for large text (18pt+ or 14pt+ bold)
- **1.4.4 Resize Text (AA)**: Text can be resized to 200% without loss
- **1.4.5 Images of Text (AA)**: Use actual text instead of images
- **1.4.10 Reflow (AA)**: Content reflows without scrolling in two directions
- **1.4.11 Non-text Contrast (AA)**: 3:1 contrast for UI components
- **1.4.12 Text Spacing (AA)**: No loss of content when adjusting spacing
- **1.4.13 Content on Hover or Focus (AA)**: Dismissible, hoverable, persistent

### Operable

#### 2.1 Keyboard Accessible
- **2.1.1 Keyboard (A)**: All functionality available via keyboard
- **2.1.2 No Keyboard Trap (A)**: Keyboard focus can be moved away
- **2.1.4 Character Key Shortcuts (A)**: Can be turned off or remapped

#### 2.2 Enough Time
- **2.2.1 Timing Adjustable (A)**: User can extend time limits
- **2.2.2 Pause, Stop, Hide (A)**: Moving, blinking, scrolling content can be controlled

#### 2.3 Seizures and Physical Reactions
- **2.3.1 Three Flashes or Below Threshold (A)**: No content flashes more than 3 times per second

#### 2.4 Navigable
- **2.4.1 Bypass Blocks (A)**: Mechanism to skip repeated content
- **2.4.2 Page Titled (A)**: Pages have descriptive titles
- **2.4.3 Focus Order (A)**: Focus order is logical
- **2.4.4 Link Purpose (A)**: Link purpose can be determined from link text
- **2.4.5 Multiple Ways (AA)**: Multiple ways to find pages
- **2.4.6 Headings and Labels (AA)**: Headings and labels are descriptive
- **2.4.7 Focus Visible (AA)**: Keyboard focus indicator is visible
- **2.4.11 Focus Not Obscured (Minimum) (AA)**: Focus indicator not fully hidden

#### 2.5 Input Modalities
- **2.5.1 Pointer Gestures (A)**: Alternatives for complex gestures
- **2.5.2 Pointer Cancellation (A)**: Up-event for single pointer actions
- **2.5.3 Label in Name (A)**: Visible label matches accessible name
- **2.5.4 Motion Actuation (A)**: Can disable motion-activated features
- **2.5.7 Dragging Movements (AA)**: Alternatives to dragging
- **2.5.8 Target Size (Minimum) (AA)**: Targets at least 24x24 CSS pixels

### Understandable

#### 3.1 Readable
- **3.1.1 Language of Page (A)**: Page language is programmatically determined
- **3.1.2 Language of Parts (AA)**: Language of parts can be determined

#### 3.2 Predictable
- **3.2.1 On Focus (A)**: Focus doesn't trigger context change
- **3.2.2 On Input (A)**: Input doesn't trigger context change unless warned
- **3.2.3 Consistent Navigation (AA)**: Navigation is consistent
- **3.2.4 Consistent Identification (AA)**: Components are identified consistently
- **3.2.6 Consistent Help (A)**: Help mechanism in consistent location

#### 3.3 Input Assistance
- **3.3.1 Error Identification (A)**: Errors are identified in text
- **3.3.2 Labels or Instructions (A)**: Labels provided for input
- **3.3.3 Error Suggestion (AA)**: Suggestions provided for errors
- **3.3.4 Error Prevention (AA)**: Prevent errors on legal/financial/data submissions
- **3.3.7 Redundant Entry (A)**: Don't require same information multiple times
- **3.3.8 Accessible Authentication (Minimum) (AA)**: No cognitive function test for authentication

### Robust

#### 4.1 Compatible
- **4.1.1 Parsing (A)**: HTML is valid (deprecated in WCAG 2.2)
- **4.1.2 Name, Role, Value (A)**: Name and role can be programmatically determined
- **4.1.3 Status Messages (AA)**: Status messages can be programmatically determined

## New in WCAG 2.2

The following success criteria were added in WCAG 2.2:

1. **2.4.11 Focus Not Obscured (Minimum)** (AA)
2. **2.4.12 Focus Not Obscured (Enhanced)** (AAA)
3. **2.4.13 Focus Appearance** (AAA)
4. **2.5.7 Dragging Movements** (AA)
5. **2.5.8 Target Size (Minimum)** (AA)
6. **3.2.6 Consistent Help** (A)
7. **3.3.7 Redundant Entry** (A)
8. **3.3.8 Accessible Authentication (Minimum)** (AA)
9. **3.3.9 Accessible Authentication (Enhanced)** (AAA)

## Common Violations and Fixes

### Images without alt text
**Issue**: `<img src="photo.jpg">`
**Fix**: `<img src="photo.jpg" alt="Description of image">`

### Poor color contrast
**Issue**: Light gray text on white background
**Fix**: Use colors with at least 4.5:1 contrast ratio

### Missing form labels
**Issue**: `<input type="text" placeholder="Email">`
**Fix**: `<label for="email">Email</label><input type="text" id="email">`

### Missing landmark regions
**Issue**: `<div class="header">`
**Fix**: `<header>` or `<div role="banner">`

### Keyboard inaccessible
**Issue**: `<div onclick="doSomething()">Click me</div>`
**Fix**: `<button onclick="doSomething()">Click me</button>`

### Missing page language
**Issue**: `<html>`
**Fix**: `<html lang="en">`

### Empty links
**Issue**: `<a href="/page"></a>`
**Fix**: `<a href="/page">Go to page</a>`

### Improper heading hierarchy
**Issue**: `<h1>Title</h1> <h3>Subtitle</h3>`
**Fix**: `<h1>Title</h1> <h2>Subtitle</h2>`

## Testing Tools

- **axe DevTools**: Browser extension for accessibility testing
- **WAVE**: Web accessibility evaluation tool
- **NVDA/JAWS**: Screen readers for testing
- **Keyboard only**: Test all functionality with Tab, Enter, Space, Arrow keys
- **Zoom to 200%**: Ensure content remains usable

## Resources

- Official WCAG 2.2: https://www.w3.org/WAI/WCAG22/quickref/
- axe-core rules: https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md
- WebAIM: https://webaim.org/
- A11y Project: https://www.a11yproject.com/
