import os
import yaml

from time import time

MAXINT = 2147483647
CRTs = "ENHANCED_CRAFTING_TABLE, MAGIC_WORKBENCH, ARMOR_FORGE, COMPRESSOR, PRESSURE_CHAMBER, SMELTERY, ORE_CRUSHER, GRIND_STONE, ANCIENT_ALTAR, NONE".split(', ')
BIOMES = set("BADLANDS  BAMBOO_JUNGLE  BASALT_DELTAS  BEACH  BIRCH_FOREST  CHERRY_GROVE  COLD_OCEAN  CRIMSON_FOREST  CUSTOM DARK_FOREST  DEEP_COLD_OCEAN  DEEP_DARK  DEEP_FROZEN_OCEAN  DEEP_LUKEWARM_OCEAN  DEEP_OCEAN  DESERT  DRIPSTONE_CAVES  END_BARRENS  END_HIGHLANDS  END_MIDLANDS  ERODED_BADLANDS  FLOWER_FOREST  FOREST  FROZEN_OCEAN  FROZEN_PEAKS  FROZEN_RIVER  GROVE  ICE_SPIKES  JAGGED_PEAKS  JUNGLE  LUKEWARM_OCEAN  LUSH_CAVES  MANGROVE_SWAMP  MEADOW  MUSHROOM_FIELDS  NETHER_WASTES  OCEAN  OLD_GROWTH_BIRCH_FOREST  OLD_GROWTH_PINE_TAIGA  OLD_GROWTH_SPRUCE_TAIGA  PLAINS  RIVER  SAVANNA  SAVANNA_PLATEAU  SMALL_END_ISLANDS  SNOWY_BEACH  SNOWY_PLAINS  SNOWY_SLOPES  SNOWY_TAIGA  SOUL_SAND_VALLEY  SPARSE_JUNGLE  STONY_PEAKS  STONY_SHORE  SUNFLOWER_PLAINS  SWAMP  TAIGA  THE_END  THE_VOID  WARM_OCEAN  WARPED_FOREST  WINDSWEPT_FOREST  WINDSWEPT_GRAVELLY_HILLS  WINDSWEPT_HILLS  WINDSWEPT_SAVANNA  WOODED_BADLANDS".split(' '))

saveditems = set()
parentsCategories = set()
normalCategories = set()
items = set()

def report(i):
    print(f"在 {i}:", end="\n  ")

def startWith(string, target):
    if string[:len(target)] == target:
        return True
    return False

def getYamlContent(file):
    try:
        return yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError as err:
        print(f'{file}未找到')
        return {}
    except PermissionError as err:
        print('无权限')
        return {}

def RewriteSlimefunItems():
    try:
        with open('__SlimefunItems.yml', 'r', encoding='utf-8') as file:
            if getYamlContent(file)['status'] == 'well':
                return
            else:
                1/0
    except BaseException as err:  # 任何错误
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..\\Slimefun\\Items.yml")
        with open(file_path, 'r', encoding='utf-8') as file:
            regNames = getYamlContent(file).keys()
        with open('__SlimefunItems.yml', 'w', encoding='utf-8') as file:
            yaml.dump({'items':list(regNames)}, file, allow_unicode=True, encoding='utf-8')
            yaml.dump({'status':'well'}, file, allow_unicode=True, encoding='utf-8')


def getSaveditems():
    items = set()
    for root, dirs, files in os.walk("saveditems"):
        for file_name in files:
            if file_name.endswith(".yml"):
                file_name = os.path.basename(file_name)
                items.add(file_name[:-4])
    return items

def getSlimefunItems():
    with open('__SlimefunItems.yml', 'r', encoding='utf-8') as file:
        sfItems = getYamlContent(file)
    return sfItems['items']

def getVanillaItems():
    with open('__VanillaItems.yml', 'r', encoding='utf-8') as file:
        mcItems = getYamlContent(file)
    return mcItems['items']


def inSlimefun(item):
    intersection = SlimefunItems.intersection(set([item]))
    if len(intersection) == 0:
        return False
    return True

def inVanilla(item):
    intersection = VanillaItems.intersection(set([item.upper()]))
    if len(intersection) == 0:
        return False
    return True

def inSaveditems(item):
    intersection = saveditems.intersection(set([item]))
    if len(intersection) == 0:
        return False
    return True

def inBiome(item):
    intersection = BIOMES.intersection(set([item]))
    if len(intersection) == 0:
        return False
    return True

def isVanilla(item, position):
    if not startWith(item, "SKULL") and not inVanilla(item):
        report(position)
        print(f"{item} 可能不是正确的原版物品！")

def isSlimefun(item, position):
    if not inSlimefun(item) and item not in items:
        report(position)
        print(f"{item} 可能不是正确的粘液物品！")

def isSaveditem(item, position):
    if not inSaveditems(str(item)):
        report(position)
        print(f"{item} 可能不是正确的保存物品")

def isBiome(item, position):
    if not inBiome(item):
        report(position)
        print(f"{item} 可能不是正确的群系")

def isCategory(category, position):
    if not startWith(category, "existing:") and not category in normalCategories:
        report(position)
        print(f"{category} 可能不是正确的分类！")

def isItemTypeProper(data, position):
    dType = data['item-type']
    dId = data['item-id']
    if dType == "CUSTOM":
        isVanilla(dId, position+'item-id ')
    elif dType == "SAVEDITEM":
        isSaveditem(dId, position+'item-id ')
    else:
        report(position+'item-type ')
        print(f"{dType} 可能不是一个有效的类型")

def isInt(num, position, bottom=0, top=MAXINT):
    if isinstance(num, int):
        if not bottom <= num <= top:
            report(position)
            print(f"{num} 不在区间[{bottom},{top}]内")
    else:
        report(position)
        print(f"{num} 不是整数")

def isAmountProper(dAm, position):
    isInt(dAm, position, 1, 64)

def TIA(dat, position):
    dType = dat['type']
    dId = dat.get('id', 'N/A')
    dAm = dat.get('amount', 1)
    if dType == 'SLIMEFUN':
        isSlimefun(dId, position+'id ')
    elif dType == 'VANILLA':
        isVanilla(dId, position+'id ')
    elif dType == 'SAVEDITEM':
        isSaveditem(dId, position+'id ')
    elif dType == 'NONE':
        ...
    else:
        report(position+'type ')
        print('type 只能是 VANILLA, SLIMEFUN, SAVEDITEM, NONE 中的任意一个！')
    if dType != 'NONE':
        isAmountProper(dAm, position+'amount ')

def isRecipeProper(data, position):
    crt = data['crafting-recipe-type']
    if crt not in CRTs:
        print(f'{crt} 可能不是正确的配方类型')
    temp = []
    recipe = data['crafting-recipe']
    for j in recipe:
        dat = recipe[j]
        dType = dat['type']
        dId = dat.get('id', 'N/A')
        dAm = dat.get('amount', 1)
        TIA(dat, position+f'crafting-recipe 的 第 {j} 个物品 的 ')
        temp.append([dType, dId, dAm])
    idx = 1
    if crt in {'ENHANCED_CRAFTING_TABLE', 'MAGIC_WORKBENCH', 'ARMOR_FORGE', 'PRESSURE_CHAMBER'}:
        for k in temp:
            if k[2] != 1:
                report(position+f'crafting-recipe 的 第 {idx} 个物品')
                print(f'amount 必须为 1')
                break
            idx += 1
    elif crt in {'COMPRESSOR', 'PRESSURE_CHAMBER', 'ORE_CRUSHER', 'GRIND_STONE'}:
        for k in temp[1:]:
            if k[0] != 'NONE':
                report(position+f'crafting-recipe 的 第 {k} 个物品')
                print(f"2-9槽必须为NONE类型")
                break
            idx += 1
    elif crt == "ANCIENT_ALTAR":
        for k in temp:
            if k[0] == 'NONE':
                report(position+f'crafting-recipe 的 第 {idx} 个物品的 type')
                print(f"1-9槽必须不为NONE类型")
                break
            idx += 1
    elif crt == "SMELTERY":
        sum_dict = {}
        for k in temp:
            if k[0] == 'NONE':
                continue
            key = k[1]
            value = k[2]
            if key in sum_dict:
                sum_dict[key] += value
                if sum_dict[key] > 64:
                    report(position+f'第 {idx} 个物品的 amount ')
                    print(f"单种物品消耗数量不能超过64！")
                    break
            else:
                sum_dict[key] = value
            idx += 1

def isRunningRecipeProper(data, position):
    recipes = data['recipes']
    for j in recipes:
        try: 
            int(j)
        except TypeError as err:
            report('recipes ')
            print(f"{j} 不是有效的配方编号")
        recipe = recipes[j]
        speed = recipe['speed-in-seconds']
        isInt(speed, position+f'第 {j} 个配方的 speed-in-seconds')
        Input = recipe['input']
        Output = recipe['output']
        if len(Input) != 2:
            report(position+f'第 {j} 个配方的 input')
            print('input参数数量错误')
        if Input['1']['id'] == Input['2']['id'] and Input['1']['amount']+Input['2']['amount'] > 64:
            report(position+f'第 {j} 个配方的 input')
            print('input 两个输入物品相同且amount总和 > 64，这会导致一些bug！')
        for k in Input:
            TIA(Input[k], position+f'第 {j} 个配方的 input 的 ')
        if len(Output) != 2:
            report(position+f'第 {j} 个配方的 output')
            print('output参数数量错误')
        for k in Output:
            TIA(Output[k], position+f'第 {j} 个配方的 output 的 ')

def isRunningRecipeProperInGenerators(data, position):
    recipes = data['recipes']
    for j in recipes:
        recipe = recipes[j]
        speed = recipe['time-in-seconds']
        Input = recipe['input']
        Output = recipe['output']
        TIA(Input, position+'input 的 ')
        TIA(Output, position+'output 的 ')

def checkCategories():
    print('Testing categories')
    with open('categories.yml', 'r', encoding='utf-8') as file:
        k = getYamlContent(file)
    for i in k:
        data = k[i]
        item = data['category-item']
        isVanilla(item, i)
        dType = data['type']
        if dType == 'nested':
            parentsCategories.add(i)
        elif dType == 'sub':
            dParent = data['parent']
            if not startWith(dParent, "existing:"):
                if not dParent in parentsCategories:
                    report(f'categories: {i}')
                    print(f"{dParent} 可能不是正确的父分类！")
        elif dType == 'seasonal':
            dMonth = data['month']
            isInt(dMonth, f'categories: {i} 的 month', 1, 12)
        elif dType == 'normal':
            ...
        elif dType == 'locked':
            ...
        if 'tier' in data:
            dTier = data['tier']
            isInt(dTier, f'categories: {i} 的 tier')
        normalCategories.add(i)

def checkMobDrops():
    print('Testing mob-drops')
    with open('mob-drops.yml', 'r', encoding='utf-8') as file:
        k = getYamlContent(file)

    for i in k:
        data = k[i]
        dCategory = data['category']
        isCategory(dCategory, f'mob-drops: {i} 的 category')
        isItemTypeProper(data, f'mob-drops: {i} 的 ')
        dAm = data['item-amount']
        isAmountProper(dAm, f'mob-drops: {i} 的 item-amount')
        dChance = data['chance']
        isInt(dChance, f'mob-drops: {i} 的 chance', 0, 100)
        dMob = data['mob']
        if dMob not in entities:
            report(f'mob-drops: {i} 的 mob')
            print(f"{dMob} 可能不是正确的生物")
        dDisplay = data['recipe-display-item']
        isVanilla(dDisplay, f'mob-drops: {i} 的 recipe-display-item')
        items.add(i)


def checkGeoResources():
    print('Testing geo-resources')
    with open('geo-resources.yml', 'r', encoding='utf-8') as file:
        k = getYamlContent(file)

    for i in k:
        data = k[i]
        dCategory = data['category']
        isCategory(dCategory, f'geo-resouces: {i} 的 catrgory')
        isItemTypeProper(data, f'geo-resouces: {i} 的 ')
        dDev = data['max-deviation']
        isInt(dDev, f'geo-resouces: {i} 的 max-deviation', 1)
        ok = False
        if 'biome' in data:
            ok = True
            dBi = data['biome']
            for m in dBi:
                isBiome(m, f'geo-resouces: {i} 的 biome')
                isInt(dBi[m], f'geo-resouces: {i} 的 biome 的 {m}')
        if 'environment' in data:
            ok = True
            dEnv = data['environment']
            for m in dEnv:
                if m not in ("NORMAL", "NETHER", "THE_END"):
                    report(f'geo-resouces: {i} 的 environment')
                    print(f"{m} 不是正确的类型")
                isInt(dEnv[m], f'geo-resouces: {i} 的 environment 的 {m}')
        if not ok:
            report(i)
            print(f"{i} 未找到 biome 或 environment")
        items.add(i)

def checkItems():
    print("Testing items")
    with open('items.yml', 'r', encoding='utf-8') as file:
        k = getYamlContent(file)

    for i in k:
        data = k[i]
        dCategory = data['category']
        isCategory(dCategory, f'items: {i} 的 category')
        isItemTypeProper(data, f'items: {i} 的 ')
        dAm = data['item-amount']
        isAmountProper(dAm, f'items: {i} 的 item-amount')
        dPlaceable = data['placeable']
        if dPlaceable not in {True, False}:
            report(f'items: {i} 的 placeable')
            print(f"placeable 只能为 true 或 false")
        isRecipeProper(data, f'items: {i} 的 ')
        items.add(i)

def checkCapacitors():
    print('Testing capacitors')
    with open('capacitors.yml', 'r', encoding='utf-8') as file:
        k = getYamlContent(file)

    for i in k:
        data = k[i]
        dCategory = data['category']
        isCategory(dCategory, f'capacitors: {i} 的 category')
        dType = data['block-type']
        if dType not in ('DEFAULT','default'):
            isVanilla(dType, f'capacitors: {i} 的 block-type')
        dCapa = data['capacity']
        isInt(dCapa, f'acpacitors: {i} 的 capacity')
        dAm = data['item-amount']
        isAmountProper(dAm, f'capacitors: {i} 的 item-amount')
        isRecipeProper(data, f'capacitors: {i} 的 ')
        items.add(i)

def checkMachines():
    print("Testing machines")
    with open('machines.yml', 'r', encoding='utf-8') as file:
        k = getYamlContent(file)

    for i in k:
        data = k[i]
        dCategory = data['category']
        isCategory(dCategory, f'machines: {i} 的 category')
        dType = data['block-type']
        isVanilla(dType, f'machines: {i} 的 block-type')
        dBar = data['progress-bar-item']
        isVanilla(dBar, f'machines: {i} 的 progress-bar-item')
        dStats = data['stats']
        dEC = dStats['energy-consumption']
        isInt(dEC, f'machines: {i} 的 stats 的 energy-comsumption')
        dEB = dStats['energy-buffer']
        isInt(dEB, f'machines: {i} 的 stats 的 energy-buffer')
        isRecipeProper(data, f'machines: {i} 的 ')
        isRunningRecipeProper(data, f'machines: {i} 的 ')
        items.add(i)

def checkGenerators():
    print("Testing generators")
    with open('generators.yml', 'r', encoding='utf-8') as file:
        k = getYamlContent(file)

    for i in k:
        data = k[i]
        dCategory = data['category']
        isCategory(dCategory, f'generators: {i} 的 category')
        dType = data['block-type']
        isVanilla(dType, f'generators: {i} 的 block-type')
        dBar = data['progress-bar-item']
        isVanilla(dBar, f'generators: {i} 的 progress-bar-item')
        dStats = data['stats']
        dEP = dStats['energy-production']
        isInt(dEP, f'generators: {i} 的 energy-production')
        dEB = dStats['energy-buffer']
        isInt(dEB, f'generators: {i} 的 energy-buffer')
        isRecipeProper(data, f'generators: {i} 的 ')
        isRunningRecipeProperInGenerators(data, f'generators: {i} 的 ')
        items.add(i)

def checkSolarGenerators():
    print("Testing solar-generators")
    with open('solar-generators.yml', 'r', encoding='utf-8') as file:
        k = getYamlContent(file)

    for i in k:
        data = k[i]
        dCategory = data['category']
        isCategory(dCategory, f'solar-generators: {i} 的 category')
        dType = data['block-type']
        isVanilla(dType, f'solar-generators: {i} 的 block-type')
        dEP = data['stats']['energy-production']
        isInt(dEP['day'], f'solar-generators: {i} 的 stats 的 energy-production 的 day')
        isInt(dEP['night'], f'solar-generators: {i} 的 stats 的 energy-production 的 night')
        isRecipeProper(data, f'solar-generators: {i} 的 ')
        items.add(i)
def checkMaterialGenerators():
    print("Testing material-generators.yml")
    with open('material-generators.yml', 'r', encoding='utf-8') as file:
        k = getYamlContent(file)

    for i in k:
        data = k[i]
        dCategory = data['category']
        isCategory(dCategory, f'material-generators: {i} 的 category')
        dType = data['block-type']
        isVanilla(dType, f'material-generators: {i} 的 block-type')
        dStats = data['stats']
        dEC = dStats['energy-consumption']
        isInt(dEC, f'material-generators: {i} 的 energy-comsumption')
        dEB = dStats['energy-buffer']
        isInt(dEB, f'material-generators: {i} 的 energy-buffer')
        isRecipeProper(data, f'material-generators: {i} 的 ')
        output = data['output']
        tickRate = output['tick-rate']
        isInt(tickRate, f'material-generators: {i} 的 output 的 tick-rate')
        TIA(output, f'material-generators: {i} 的 output 的')
        items.add(i)

def checkResearches():
    print("Testing researches.yml")
    with open('researches.yml', 'r', encoding='utf-8') as file:
        k = getYamlContent(file)

    for i in k:
        data = k[i]
        dId = data['id']
        isInt(dId, f'researches: {i} 的 id')
        dCost = data['cost']
        isInt(dCost, f'researches: {i} 的 cost')

sum_start = time()
checkers = [
    checkCategories,
    checkMobDrops,
    checkGeoResources,
    checkItems,
    checkCapacitors,
    checkMachines,
    checkGenerators,
    checkSolarGenerators,
    checkMaterialGenerators,
    checkResearches
]
def checkAll():
    for i in checkers:
        start = time()
        try:
            i()
        except (yaml.scanner.ScannerError, yaml.parser.ParserError) as err:
            print('在获取YAML内容时遇到了错误！')
            print('可能是YAML结构错误！请在下方网站内检查')
            print('https://www.bejson.com/validators/yaml_editor/')
        except FileNotFoundError as err:
            print('未找到文件！')
        except TypeError as err:
            print('未从YAML中获取到内容')
            print('你是否删除了这个YAML中的所有内容?')
        print(f'Spent {time() - start}s')
    print(f"Sum {time() - sum_start}s")
RewriteSlimefunItems()
SlimefunItems = set(getSlimefunItems())
VanillaItems = set(getVanillaItems())
saveditems = getSaveditems()
entities = set()
for i in VanillaItems:
    if i[-10:] == '_SPAWN_EGG':
        entities.add(i[:-10])
entities.add("GIANT")

"""
'请确保控制台输出的bug（若有）皆已修复，本程序才能正常运行！'
'需要注意的是，本py并不会检查任何与name或lore相关的内容！'
'如有误报请联系作者企鹅2793572961'
'此python程序任何人皆可使用，修改，但不得进行任何商业活动、违反公德的行为或违法行为'
'Made by guguguhello'
"""

checkAll()
