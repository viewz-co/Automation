# 🔄 Entity Selection Refactoring Guide

## Overview
This guide shows how to refactor your existing Playwright tests to include entity selection after login.

## 🎯 New Pattern: Login → Entity Selection → Test

### Before (Old Pattern):
```python
@pytest.mark.asyncio
async def test_something(perform_login):
    page = perform_login
    # Test logic starts immediately after login
```

### After (New Pattern):
```python
@pytest.mark.asyncio  
async def test_something(perform_login_with_entity):
    page = perform_login_with_entity
    # Entity is already selected, test logic proceeds
```

## 🛠️ What Was Added

### 1. EntitySelectorPage (`pages/entity_selector_page.py`)
```python
from pages.entity_selector_page import EntitySelectorPage

entity_selector = EntitySelectorPage(page)
await entity_selector.select_entity("Viewz Demo INC")
```

### 2. Enhanced Login Fixture (`tests/conftest.py`)
```python
@pytest_asyncio.fixture
async def perform_login_with_entity(page, login_data):
    # 1. Login with 2FA
    # 2. Select Entity
    # 3. Return page ready for testing
```

## 📋 Migration Strategies

### Strategy 1: Gradual Migration (Recommended)

**Step 1:** Keep existing tests working
```python
# OLD - Still works
async def test_old_way(perform_login):
    page = perform_login
    
# NEW - With entity selection  
async def test_new_way(perform_login_with_entity):
    page = perform_login_with_entity
```

**Step 2:** Migrate tests one by one
- Choose high-priority tests first
- Test entity-dependent functionality
- Migrate systematically

### Strategy 2: Complete Replacement

**Replace all at once:**
```bash
# Find and replace across all test files
find tests/ -name "*.py" -exec sed -i '' 's/perform_login/perform_login_with_entity/g' {} \;
```

## 🔄 File-by-File Migration Examples

### Navigation Tests
```python
# Before
async def test_tab_navigation(perform_login, text, page_class):
    page = perform_login

# After  
async def test_tab_navigation(perform_login_with_entity, text, page_class):
    page = perform_login_with_entity
```

### Bank Tests
```python
# Before
@pytest_asyncio.fixture
async def bank_page(self, page: Page, login_data):
    # Manual login logic
    login = LoginPage(page)
    await login.goto()
    # ... login code ...

# After
@pytest_asyncio.fixture
async def bank_page(self, page: Page):
    # Use the enhanced fixture
    bank = BankPage(page)
    return bank

# Test method changes
async def test_bank_operations(perform_login_with_entity):
    page = perform_login_with_entity
    bank = BankPage(page)
    await bank.navigate_to_bank()
```

### Payables Tests
```python
# Before
@pytest_asyncio.fixture
async def payables_page(self, page: Page, login_data):
    # Manual login + navigation

# After
@pytest_asyncio.fixture  
async def payables_page(self, page: Page):
    # Just create page object, login handled by test
    return PayablesPage(page)

async def test_payables(perform_login_with_entity, payables_page):
    page = perform_login_with_entity
    await payables_page.navigate_to_payables()
```

## 🧪 Testing Entity Selection

### Validate Entity Selection Works
```python
@pytest.mark.asyncio
async def test_entity_selection_validation(perform_login_with_entity):
    page = perform_login_with_entity
    
    from pages.entity_selector_page import EntitySelectorPage
    entity_selector = EntitySelectorPage(page)
    
    # Verify entity is selected
    verified = await entity_selector.verify_entity_selected("Viewz Demo INC")
    assert verified, "Entity selection failed"
    
    # Get available entities
    entities = await entity_selector.get_available_entities()
    print(f"Available entities: {entities}")
```

## 📝 Migration Checklist

### Phase 1: Setup (✅ Complete)
- [x] Create EntitySelectorPage
- [x] Add perform_login_with_entity fixture
- [x] Create sample refactored test

### Phase 2: Test Migration
Choose your approach:

#### Option A: Gradual Migration
- [ ] **Navigation Tests**: Replace `perform_login` → `perform_login_with_entity`
  - `tests/e2e/navigation/test_tabs_navigation.py`
  - `tests/e2e/navigation/test_tabs_navigation_single_login.py`

- [ ] **Bank Tests**: Update fixtures and test methods
  - `tests/e2e/reconciliation/bank/test_bank_operations.py`

- [ ] **Payables Tests**: Update fixtures and test methods  
  - `tests/e2e/reconciliation/payables/test_payables_operations.py`
  - `tests/e2e/reconciliation/payables/test_complete_payables_operations.py`

- [ ] **Login Tests**: Add entity validation
  - `tests/e2e/login/test_login_scenarios.py`

- [ ] **API Tests**: Add entity context if needed
  - `tests/api/test_date_format_validation.py`

#### Option B: Complete Replacement
- [ ] **Global Replace**: `perform_login` → `perform_login_with_entity`
- [ ] **Test All**: Run full test suite
- [ ] **Fix Issues**: Address any entity-specific failures

### Phase 3: Validation
- [ ] **Test Entity Selection**: Verify entity picker works
- [ ] **Test All Modules**: Ensure all tests pass with entity context
- [ ] **TestRail Integration**: Verify results still mark correctly
- [ ] **Documentation**: Update test documentation

## 🎯 Quick Migration Commands

### Replace in Navigation Tests
```bash
sed -i '' 's/perform_login)/perform_login_with_entity)/g' tests/e2e/navigation/test_tabs_navigation.py
```

### Replace in Bank Tests  
```bash
sed -i '' 's/perform_login)/perform_login_with_entity)/g' tests/e2e/reconciliation/bank/test_bank_operations.py
```

### Replace in Payables Tests
```bash
sed -i '' 's/perform_login)/perform_login_with_entity)/g' tests/e2e/reconciliation/payables/test_*.py
```

## ⚠️ Important Considerations

### Entity-Dependent Tests
Some tests may need specific entities:
```python
# Custom entity selection
entity_selector = EntitySelectorPage(page)
await entity_selector.select_entity("Different Company INC")
```

### Error Handling
Entity selection might fail:
```python
# In your tests, handle entity selection gracefully
entity_selected = await entity_selector.select_entity("Viewz Demo INC")
if not entity_selected:
    pytest.skip("Entity selection failed - may not be required for this test")
```

### TestRail Mapping
Tests with new names need TestRail mapping:
```python
# Add to conftest.py case_mapping
'test_with_entity_selection': 12345,
```

## 🚀 Benefits After Migration

1. **✅ Consistent Entity Context** - All tests run with proper entity selection
2. **✅ Realistic Test Scenarios** - Tests reflect actual user workflow
3. **✅ Entity-Specific Data** - Tests see data relevant to selected entity
4. **✅ Reduced Test Flakiness** - Proper entity context reduces timing issues
5. **✅ Better Test Coverage** - Entity selection functionality is tested

## 🎯 Next Steps

1. **Choose Migration Strategy** (Gradual vs Complete)
2. **Start with High-Priority Tests** (Navigation, Core Functionality)
3. **Test Incrementally** (Verify each migrated test works)
4. **Update Documentation** (Record any entity-specific requirements)

---

**Ready to start migration? Choose your approach and begin with the navigation tests!** 🚀 