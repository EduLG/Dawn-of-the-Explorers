import React from "react";
import { Avatar, Card } from "@radix-ui/themes";
import scholar from "../assets/resources/character-templates/scholar_male.png";

const CharacterCard = () => {
  return (
    <Card className="relative bg-gradient-to-b from-white/9 to-white/3 rounded-xl overflow-hidden border border-white/6 shadow-lg hover:scale-[1.02] transition-transform duration-200">
      <div className="bg-gradient-to-r rounded-md from-[#5b3e1f]/80 to-[#3b2720]/60 border-b border-white/6 px-4 py-2">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm text-[#e6d3a3]">Aldric</div>
            <div className="text-xs text-[#f3e5c8]">Class: Adventurer</div>
          </div>

          <div className="flex items-center gap-2">
            <div className="text-xs text-[#e6d3a3]">Rating</div>
            <div className="bg-[#ffefe0]/90 text-[#3b2a1a] font-semibold px-3 py-1 rounded-full shadow-sm">
              320
            </div>
          </div>
        </div>
      </div>

      <div className="p-4 h-full flex flex-col md:flex-row items-center md:items-stretch gap-4">
        <div className="flex-shrink-0 flex items-center justify-center md:pl-2">
          <div className="w-28 h-28 rounded-full bg-[#e6d3a3] p-1 flex items-center justify-center">
            <Avatar src={scholar} size="7" />
          </div>
        </div>

        <div className="flex-1 flex flex-col justify-center w-full">
          <div className="w-full mt-0 text-sm text-[#6b4f2a]">
            <div className="flex items-start justify-between w-full">
              <div className="flex-1">
                <div className="text-xs text-[#e6d3a3]">Type</div>
                <ul className="mt-1 space-y-1 text-[#3b2a1a]">
                  <li>Primary arm</li>
                  <li>Secondary arm</li>
                  <li>Head</li>
                  <li>Chest</li>
                  <li>Accessory</li>
                </ul>
              </div>

              <div className="flex-1 text-right">
                <div className="text-xs text-[#e6d3a3]">Equipped</div>
                <ul className="mt-1 space-y-1 text-[#3b2a1a]">
                  <li>Iron Sword</li>
                  <li>Iron Shield</li>
                  <li>Helmet</li>
                  <li>Steel Chest</li>
                  <li>Silver Ring</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default CharacterCard;
