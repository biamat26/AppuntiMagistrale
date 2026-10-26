-- Trasforma i div ::: {.classe} nei riquadri tcolorbox definiti in main.tex.
local envs = { inbreve = true, esempio = true, nota = true, approfondimento = true }

local function latex_of(str)
  local doc = pandoc.read(str, 'markdown')
  local out = pandoc.write(doc, 'latex')
  return (out:gsub('%s+$', ''))
end

function Div(el)
  for _, cls in ipairs(el.classes) do
    if envs[cls] then
      local open = '\\begin{' .. cls .. '}'
      if cls == 'approfondimento' then
        open = open .. '{' .. latex_of(el.attributes.title or '') .. '}'
      end
      local blocks = { pandoc.RawBlock('latex', open) }
      for _, b in ipairs(el.content) do table.insert(blocks, b) end
      table.insert(blocks, pandoc.RawBlock('latex', '\\end{' .. cls .. '}'))
      return blocks
    end
  end
end
