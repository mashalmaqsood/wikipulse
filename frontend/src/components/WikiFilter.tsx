import * as Select from "@radix-ui/react-select";
import { Check, ChevronDown } from "lucide-react";

interface WikiFilterProps {
  wikis: string[];
  selected: string;
  onChange: (wiki: string) => void;
}

export const ALL_WIKIS = "all";

export function WikiFilter({ wikis, selected, onChange }: WikiFilterProps) {
  return (
    <div className="wiki-filter">
      <span className="wiki-filter__label">Wiki</span>
      <Select.Root value={selected} onValueChange={onChange}>
        <Select.Trigger className="wiki-filter__trigger" aria-label="Filter by wiki">
          <Select.Value />
          <Select.Icon className="wiki-filter__chevron">
            <ChevronDown size={14} />
          </Select.Icon>
        </Select.Trigger>
        <Select.Portal>
          <Select.Content className="wiki-filter__content" position="popper" sideOffset={6}>
            <Select.Viewport className="wiki-filter__viewport">
              <Select.Item value={ALL_WIKIS} className="wiki-filter__item">
                <Select.ItemText>All wikis</Select.ItemText>
                <Select.ItemIndicator className="wiki-filter__item-indicator">
                  <Check size={14} />
                </Select.ItemIndicator>
              </Select.Item>
              {wikis.map((wiki) => (
                <Select.Item key={wiki} value={wiki} className="wiki-filter__item">
                  <Select.ItemText>{wiki}</Select.ItemText>
                  <Select.ItemIndicator className="wiki-filter__item-indicator">
                    <Check size={14} />
                  </Select.ItemIndicator>
                </Select.Item>
              ))}
            </Select.Viewport>
          </Select.Content>
        </Select.Portal>
      </Select.Root>
    </div>
  );
}
