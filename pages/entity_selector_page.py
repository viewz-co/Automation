"""
Entity Selector Page Object
Handles entity selection functionality after login
"""

from playwright.async_api import Page
import asyncio


class EntitySelectorPage:
    """Page object for entity selection functionality"""
    
    def __init__(self, page: Page):
        self.page = page
        
        # Entity selector elements (based on screenshot showing "Viewz Demo INC")
        self.entity_selectors = [
            # Main entity dropdown button
            'button:has-text("Viewz Demo INC")',
            'button:has-text("Demo")',
            '[data-testid="entity-selector"]',
            '[data-testid="company-selector"]',
            
            # Generic entity/company selectors
            'button[aria-expanded]:has-text("INC")',
            'button[aria-expanded]:has-text("Demo")',
            '.entity-selector',
            '.company-selector',
            
            # Dropdown patterns
            'select[name*="entity"]',
            'select[name*="company"]',
            
            # By text content
            'text=Viewz Demo INC',
            
            # Header area selectors
            'header button:has-text("Demo")',
            'nav button:has-text("Demo")',
            
            # Generic dropdown in header
            'header button[aria-expanded]',
            'header .dropdown-toggle'
        ]
        
        # Entity option selectors for dropdown
        self.entity_option_selectors = [
            '[role="menuitem"]',
            '[role="option"]',
            '.dropdown-item',
            '.entity-option',
            '.company-option',
            'li[role="option"]',
            'div[role="option"]'
        ]
    
    async def select_entity(self, entity_name: str = "Viewz Demo INC"):
        """
        Select an entity after login
        
        Args:
            entity_name: Name of the entity to select (default: "Viewz Demo INC")
        """
        try:
            print(f"🏢 Attempting to select entity: {entity_name}")
            
            # Wait for page to load after login
            await asyncio.sleep(2)
            
            # First, check if entity is already selected
            if await self._is_entity_selected(entity_name):
                print(f"✅ Entity '{entity_name}' already selected")
                return True
            
            # Find and click entity selector dropdown
            entity_button = await self._find_entity_selector()
            if not entity_button:
                print("⚠️ No entity selector found - entity selection may not be required")
                return True  # Continue with tests even if no entity selector
            
            # Click to open dropdown
            await entity_button.click()
            await asyncio.sleep(1)
            
            # Select the desired entity
            success = await self._select_entity_option(entity_name)
            if success:
                print(f"✅ Successfully selected entity: {entity_name}")
                await asyncio.sleep(2)  # Wait for entity change to process
                return True
            else:
                print(f"⚠️ Could not find entity option: {entity_name}")
                # Press Escape to close dropdown
                await self.page.keyboard.press("Escape")
                return False
                
        except Exception as e:
            print(f"❌ Error selecting entity: {str(e)}")
            return False
    
    async def _find_entity_selector(self):
        """Find the entity selector button/dropdown"""
        for selector in self.entity_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible():
                    print(f"✅ Found entity selector: {selector}")
                    return element
            except Exception:
                continue
        return None
    
    async def _select_entity_option(self, entity_name: str):
        """Select entity option from dropdown"""
        # Try to find entity option by text
        entity_text_selectors = [
            f'text={entity_name}',
            f'[role="menuitem"]:has-text("{entity_name}")',
            f'[role="option"]:has-text("{entity_name}")',
            f'.dropdown-item:has-text("{entity_name}")',
            f'li:has-text("{entity_name}")',
            f'div:has-text("{entity_name}")'
        ]
        
        for selector in entity_text_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible():
                    await element.click()
                    print(f"✅ Clicked entity option: {selector}")
                    return True
            except Exception:
                continue
        
        # If exact match not found, try partial match
        for selector in self.entity_option_selectors:
            try:
                options = self.page.locator(selector)
                count = await options.count()
                
                for i in range(count):
                    option = options.nth(i)
                    if await option.is_visible():
                        text_content = await option.text_content()
                        if text_content and entity_name.lower() in text_content.lower():
                            await option.click()
                            print(f"✅ Selected entity by partial match: {text_content}")
                            return True
            except Exception:
                continue
                
        return False
    
    async def _is_entity_selected(self, entity_name: str):
        """Check if the entity is already selected"""
        # Look for entity name in various places where it might be displayed
        check_selectors = [
            f'text={entity_name}',
            f'button:has-text("{entity_name}")',
            f'.selected-entity:has-text("{entity_name}")',
            f'.current-entity:has-text("{entity_name}")',
            f'[aria-label*="{entity_name}"]'
        ]
        
        for selector in check_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible():
                    return True
            except Exception:
                continue
        return False
    
    async def get_available_entities(self):
        """Get list of available entities"""
        try:
            # Find and click entity selector
            entity_button = await self._find_entity_selector()
            if not entity_button:
                return []
            
            await entity_button.click()
            await asyncio.sleep(1)
            
            # Get all entity options
            entities = []
            for selector in self.entity_option_selectors:
                try:
                    options = self.page.locator(selector)
                    count = await options.count()
                    
                    for i in range(count):
                        option = options.nth(i)
                        if await option.is_visible():
                            text_content = await option.text_content()
                            if text_content and text_content.strip():
                                entities.append(text_content.strip())
                except Exception:
                    continue
            
            # Close dropdown
            await self.page.keyboard.press("Escape")
            
            # Remove duplicates
            return list(set(entities))
            
        except Exception as e:
            print(f"❌ Error getting available entities: {str(e)}")
            return []
    
    async def verify_entity_selected(self, entity_name: str):
        """Verify that the correct entity is selected"""
        try:
            # Check URL for entity reference
            current_url = self.page.url
            if entity_name.lower().replace(" ", "").replace("inc", "") in current_url.lower():
                print(f"✅ Entity verified in URL: {current_url}")
                return True
            
            # Check page content
            if await self._is_entity_selected(entity_name):
                print(f"✅ Entity verified in page content")
                return True
            
            print(f"⚠️ Could not verify entity selection: {entity_name}")
            return False
            
        except Exception as e:
            print(f"❌ Error verifying entity: {str(e)}")
            return False 