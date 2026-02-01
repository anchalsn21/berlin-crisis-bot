/**
 * cn utility function
 * Combines class names with conditional logic (similar to clsx/tailwind-merge)
 */

export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}






