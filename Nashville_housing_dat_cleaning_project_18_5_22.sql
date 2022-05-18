--Kickoff by Populalting the Property Address


select *
from PortfolioProject.dbo.NashvilleHousing


--Format date using convert

select SaleDateconverted, Convert(Date,SaleDate)
from PortfolioProject.dbo.NashvilleHousing

update NashvilleHousing
set SaleDate = Convert(Date,SaleDate)

alter table NashvilleHousing
add SaleDateconverted Date;

update NashvilleHousing
set SaleDateconverted = Convert(Date,SaleDate)


-- Secondly we populate the property Addresss. We will be using selfjoin, ISNULL

select *
from PortfolioProject.dbo.NashvilleHousing
where PropertyAddress is NULL
order by ParcelID

select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, isnull(a.PropertyAddress,b.PropertyAddress)
from PortfolioProject.dbo.NashvilleHousing a
join PortfolioProject.dbo.NashvilleHousing b
	on a.ParcelID = b.ParcelID
	and a.[UniqueID ] <> b.[UniqueID ]
where a.PropertyAddress is NULL

update a
set PropertyAddress = isnull(a.PropertyAddress,b.PropertyAddress)
from PortfolioProject.dbo.NashvilleHousing a
join PortfolioProject.dbo.NashvilleHousing b
	on a.ParcelID = b.ParcelID
	and a.[UniqueID ] <> b.[UniqueID ]
where a.PropertyAddress is NULL


-- We will break the address into individual columns (address, city, state) using 'substring' and 'Charindex'.


select PropertyAddress
from PortfolioProject.dbo.NashvilleHousing
--where PropertyAddress is NULL
--order by ParcelID

select 
substring(PropertyAddress, 1, charindex(',', PropertyAddress)-1) as Address
,	substring(PropertyAddress, charindex(',', PropertyAddress)+1 , len(PropertyAddress)) as Address
from PortfolioProject.dbo.NashvilleHousing



alter table PortfolioProject.dbo.NashvilleHousing
add PropertysplitAddress Nvarchar(255);

update PortfolioProject.dbo.NashvilleHousing
set PropertysplitAddress = substring(PropertyAddress, 1, charindex(',', PropertyAddress)-1)



alter table PortfolioProject.dbo.NashvilleHousing
add PropertysplitCity Nvarchar(255);

update PortfolioProject.dbo.NashvilleHousing
set PropertysplitCity = substring(PropertyAddress, charindex(',', PropertyAddress)+1 , len(PropertyAddress)) 

select *
from PortfolioProject.dbo.NashvilleHousing

-- Next we will seperatate the OwnerAddress using Parsename

select OwnerAddress
from PortfolioProject.dbo.NashvilleHousing

select
parsename(replace(OwnerAddress, ',', '.'), 3)
,	parsename(replace(OwnerAddress, ',', '.'), 2)
,	parsename(replace(OwnerAddress, ',', '.'), 1)
from PortfolioProject.dbo.NashvilleHousing 



alter table PortfolioProject.dbo.NashvilleHousing
add OwnersplitAddress Nvarchar(255);

update PortfolioProject.dbo.NashvilleHousing
set OwnersplitAddress = parsename(replace(OwnerAddress, ',', '.'), 3)



alter table PortfolioProject.dbo.NashvilleHousing
add OwnersplitCity Nvarchar(255);

update PortfolioProject.dbo.NashvilleHousing
set OwnersplitCity = parsename(replace(OwnerAddress, ',', '.'), 2)


alter table PortfolioProject.dbo.NashvilleHousing
add OwnersplitState Nvarchar(255);

update PortfolioProject.dbo.NashvilleHousing
set OwnersplitState = parsename(replace(OwnerAddress, ',', '.'), 1)


select *
from PortfolioProject.dbo.NashvilleHousing



-- Next is to change Y ad N to Yes and No "Sold as vacant field) using 'CASE WHEN'


select distinct(SoldAsVacant), count(SoldAsVacant)
from PortfolioProject.dbo.NashvilleHousing
group by SoldAsVacant
Order by 2


select SoldAsVacant
,	case when SoldAsVacant = 'Y' then 'Yes'
		when SoldAsVacant = 'N' then 'No'
		else SoldAsVacant
		End
from PortfolioProject.dbo.NashvilleHousing

update PortfolioProject.dbo.NashvilleHousing
set SoldAsVacant = case when SoldAsVacant = 'Y' then 'Yes'
		when SoldAsVacant = 'N' then 'No'
		else SoldAsVacant
		End





-- Removing duplicates using row_number, partition by and CTE


with RowNumCTE as(
select *,
	row_number() over(
	partition by ParcelID,
				 PropertyAddress,
				 SalePrice,
				 SaleDate,
				 LegalReference
				 order by 
					UniqueID
					) row_num
				 
from PortfolioProject.dbo.NashvilleHousing
--order by ParcelID
)
delete
from RowNumCTE
where row_num > 1
--order by PropertyAddress


-- We will now delete unused columns

select *
from PortfolioProject.dbo.NashvilleHousing

alter table PortfolioProject.dbo.NashvilleHousing
drop column OwnerAddress, TaxDistrict, PropertyAddress

alter table PortfolioProject.dbo.NashvilleHousing
drop column SaleDate