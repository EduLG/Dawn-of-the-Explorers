import React from "react";
import { Avatar, Card } from "@radix-ui/themes";

const CharacterCard = ({
  charName,
  characterClass,
  rating,
  icon,
  primaryArm,
  secondaryArm,
  head,
  chest,
  accesory,
}) => {
  return (
    <Card className="relative bg-gradient-to-b from-white/9 to-white/3 rounded-xl overflow-hidden border border-white/6 shadow-lg hover:scale-[1.02] transition-transform duration-200">
      <div className="bg-gradient-to-r rounded-md from-[#5b3e1f]/80 to-[#3b2720]/60 border-b border-white/6 px-4 py-3">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div className="min-w-0">
            <div className="text-[10px] uppercase tracking-[0.2em] text-[#e6d3a3]">
              Character
            </div>
            <div className="mt-1 flex flex-col gap-2 sm:flex-row sm:items-center sm:gap-3">
              <div className="inline-flex w-fit items-center rounded-md border border-[#f1d59b]/60 bg-[#2b1b11]/60 px-2 py-0.5 text-xs font-bold uppercase tracking-wide text-[#ffe7b2]">
                {charName}
              </div>
              <div className="text-sm font-semibold text-[#f7e7c3]">
                <span className="text-[#e6d3a3]">Class:</span> {characterClass}
              </div>
            </div>
          </div>

          <div className="flex items-center justify-end gap-2 sm:min-w-[112px]">
            <div className="text-xs uppercase tracking-wide text-[#e6d3a3]">
              Rating
            </div>
            <div className="min-w-12 rounded-full bg-[#ffefe0]/90 px-3 py-1 text-center font-semibold text-[#3b2a1a] shadow-sm">
              {rating}
            </div>
          </div>
        </div>
      </div>

      <div className="p-4 h-full flex flex-col md:flex-row items-center md:items-stretch gap-4">
        <div className="flex-shrink-0 flex items-center justify-center md:pl-2">
          <div className="w-28 h-28 rounded-full bg-[#e6d3a3] p-1 flex items-center justify-center">
            <Avatar src={icon} size="7" />
          </div>
        </div>

        <div className="flex-1 flex flex-col justify-center w-full">
          <div className="w-full mt-0 text-sm text-[#6b4f2a]">
            <div className="flex items-start justify-between w-full">
              <div className="flex-1">
                <div className="text-xs text-[#e6d3a3]">Equipment</div>
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
                  <li>{primaryArm}</li>
                  <li>{secondaryArm}</li>
                  <li>{head}</li>
                  <li>{chest}</li>
                  <li>{accesory}</li>
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
