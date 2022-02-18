LuaTool = {}
function LuaTool.PrintLuaTable(datas,fileName)
    --print("excute lua function [PrintLuaTable]") 
    --print(datas,fileName)
    local mainKeyData = datas
    local subKeyData = nil
    local realData = nil
    if(mainKeyData == nil or table_is_empty(mainKeyData))then
        return nil
    end
    for key,value in pairs(mainKeyData)do
        if(table_is_empty(value))then
            return nil
        end
    end
    for key,value in pairsByKeys(mainKeyData)do
        for subKey,subValue in pairsByKeys(value)do
            --print(fileName..":"..tostring(key)..":"..tostring(subKey)..":"..type(subKey))
            if(type(subKey)=="number")then
                subKeyData = value
                break
            elseif(type(subKey)=="string" and stringIsKey(subValue,subKey))then
                subKeyData = value
                break
            else
                realData = value
                break      
            end
        end
        break
    end
    if subKeyData ~= nil then
        for key,value in pairsByKeys(subKeyData)do
            realData = value
            break
        end
    end
    local mappingTab,excelData = getMappingTabAndExcelMap(realData)
    for key,value in pairsByKeys(mainKeyData)do
        if(subKeyData ~= nil)then
            setSubKeyData(value,mappingTab,excelData)          
        else
            setExcelData(value,mappingTab,excelData)
        end    
    end
    return excelData
end
 
function table_is_empty(t)
    return _G.next(t) == nil
end
 
function stringIsKey(tab,targetKey)
    --print(LuaTool.IsArrayTable(tab))
    if LuaTool.IsArrayTable(tab) == 1 then
        for key,value in pairsByKeys(tab)do
            --print(type(targetKey)..type(value))
            if type(targetKey) == type(value) and targetKey == value then              
                return true
            end
        end
    end
    return false
end
function LuaTool.IsArrayTable(t)
    if type(t) ~= "table" then
        return 0
    end
    --[[
    local n = #t
    for i,v in pairs(t) do
        if type(i) ~= "number" then
            return false
        end
         
        if i > n then
            return false
        end
    end
    --]]
    return 1
end
function pairsByKeys(t)
    local a = {}
 
    for n in pairs(t) do
        a[#a + 1] = n
    end
 
    table.sort(a)
 
    local i = 0
         
    return function()
        i = i + 1
        return a[i], t[a[i]]
    end
end
 
function setSubKeyData(subKeyData,mapping,originTab)
    for key,value in pairsByKeys(subKeyData)do
        setExcelData(value,mapping,originTab)
    end
end
 
function setExcelData(oneData,mapping,originTab)
    local showTab = {}
    for key,value in pairs(oneData)do
        showTab[mapping[key]] = value
    end
    table.insert(originTab,showTab)
    --originTab[index] = showTab
end
function getMappingTabAndExcelMap(realData)
    local mappingTab = {}
    local excelData = {}
    excelData[1] = {}
    excelData[2] = {}
    local index = 1
    for key,value in pairsByKeys(realData)do
        mappingTab[key] = index
        excelData[1][index] = key
        local typeName = type(value)
        if(typeName == "table")then
            typeName = "Items"
        elseif(typeName == "string")then
            typeName = "String"
        elseif(typeName == "number")then
            typeName = "Number"
        end
        excelData[2][index] = typeName
        index=index+1
    end
    return mappingTab,excelData
end
 
return LuaTool